import os
import re
import time
import torch
import nltk
import pyttsx3
import pyautogui
import pyperclip
from nltk.tokenize import sent_tokenize
from transformers import pipeline, BartTokenizer

# --------------------------------------------------------------------------
# 1. Environment Configuration
# --------------------------------------------------------------------------
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'  # Enables synchronous error reporting
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppresses TensorFlow logs
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disables oneDNN optimizations

# --------------------------------------------------------------------------
# 2. Initialization
# --------------------------------------------------------------------------
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
tts_engine = pyttsx3.init()

def configure_tts(rate=150, volume=1.0, voice_id=None):
    try:
        tts_engine.setProperty('rate', rate)
        tts_engine.setProperty('volume', volume)
        if voice_id:    
            tts_engine.setProperty('voice', voice_id)
    except Exception as e:
        print(f"[ERROR] Failed to configure TTS properties. Error: {e}")

def set_voice():
    voices = tts_engine.getProperty('voices')
    for voice in voices:
        if "Microsoft Zira Desktop" in voice.name:
            tts_engine.setProperty('voice', voice.id)
            print("Voice set to Microsoft Zira Desktop.")
            return
    print("[WARNING] Microsoft Zira Desktop voice not found. Using default voice.")

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# --------------------------------------------------------------------------
# 3. Utility Functions
# --------------------------------------------------------------------------
def get_selected_text():
    """
    Simulates Ctrl+A and Ctrl+C to copy the selected text to the clipboard.
    """
    time.sleep(0.3)  # Slight delay to ensure correct timing
    pyautogui.hotkey('ctrl', 'a')  # Select all text
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')  # Copy the selected text
    time.sleep(0.3)
    return pyperclip.paste()  # Retrieve the copied text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def split_text(text, max_tokens=800):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(tokenizer.encode(sentence, add_special_tokens=False))
        if current_tokens + sentence_tokens > max_tokens:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
                current_tokens = sentence_tokens
            else:
                words = sentence.split()
                for word in words:
                    word_tokens = len(tokenizer.encode(word, add_special_tokens=False))
                    if current_tokens + word_tokens > max_tokens:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                            current_chunk = word
                            current_tokens = word_tokens
                        else:
                            chunks.append(word)
                            current_chunk = ""
                            current_tokens = 0
                    else:
                        current_chunk += " " + word
                        current_tokens += word_tokens
        else:
            current_chunk += " " + sentence
            current_tokens += sentence_tokens

    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def explain_text(text, batch_size=8, target_sentences=4, max_tokens=160, min_tokens=120):
    try:
        summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            framework="pt",
            device=0 if torch.cuda.is_available() else -1
        )

        device = "cuda:0" if torch.cuda.is_available() else "CPU"
        print(f"Device set to use {device}")

        chunks = split_text(text, max_tokens=800)
        print(f"[DEBUG] Number of chunks: {len(chunks)}")

        batched_chunks = [chunks[i:i + batch_size] for i in range(0, len(chunks), batch_size)]
        summaries = []

        for batch_num, batch in enumerate(batched_chunks, 1):
            try:
                print(f"[DEBUG] Summarizing batch {batch_num} with {len(batch)} chunks.")
                batch_summaries = summarizer(
                    batch,
                    max_length=max_tokens,
                    min_length=min_tokens,
                    num_beams=4,
                    do_sample=False
                )
                for summary in batch_summaries:
                    summaries.append(summary['summary_text'])
            except Exception as e:
                print(f"[ERROR] Summarization failed for batch {batch_num}: {e}")
                continue

        if not summaries:
            print("[INFO] No summaries generated.")
            return "[INFO] Unable to explain the text."

        full_summary = ' '.join(summaries)
        sentences = sent_tokenize(full_summary)
        trimmed_summary = ' '.join(sentences[:target_sentences])
        return trimmed_summary
    except Exception as e:
        print(f"[ERROR] Summarization failed: {e}")
        return "[INFO] Unable to explain the text."

def speak_text(text):
    try:
        set_voice()
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"[ERROR] Failed to speak text. Error: {e}")

# --------------------------------------------------------------------------
# 4. Main Function
# --------------------------------------------------------------------------
def main():
    print("[INFO] Automatically summarizing all text in the active window...")

    # Automatically select and copy all text
    selected_text = get_selected_text()

    if selected_text:
        print("[DEBUG] Selected Text:", selected_text[:200])  # Print a sample of the text
        summary = explain_text(selected_text, batch_size=8, target_sentences=4)
        print("\n[SUMMARY]:")
        print(summary)
        speak_text(summary)
    else:
        print("[INFO] No text selected or copied.")

if __name__ == "__main__":
    set_voice()
    main()
