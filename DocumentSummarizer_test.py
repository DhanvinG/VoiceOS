import os
import re
import time
import openai
import pyautogui
import pyperclip
from nltk.tokenize import sent_tokenize
from pydub import AudioSegment
from pydub.playback import play

# --------------------------------------------------------------------------
# 1. Environment Configuration
# --------------------------------------------------------------------------
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppresses TensorFlow logs

openai.api_key = yourkey

# --------------------------------------------------------------------------
# 2. Utility Functions
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

# --------------------------------------------------------------------------
# 3. GPT-4 Summarization (Updated for OpenAI v1.0.0+)
# --------------------------------------------------------------------------
def summarize_with_gpt(text, target_sentences=4):
    """
    Uses GPT-4 to summarize the given text.
    """
    try:
        print("[INFO] Sending text to GPT-4 for summarization...")

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text in {target_sentences} sentences:\n\n{text}"}
            ]
        )

        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"[ERROR] GPT-4 summarization failed: {e}")
        return "[INFO] Unable to summarize the text."

# --------------------------------------------------------------------------
# 4. ChatGPT Voice TTS (Updated for OpenAI v1.0.0+)
# --------------------------------------------------------------------------
def speak_text(text):
    """
    Uses OpenAI's text-to-speech API to read the text aloud using ChatGPT's voice.
    """
    try:
        print("[INFO] Generating speech with ChatGPT Voice...")

        # OpenAI's TTS API call
        response = openai.audio.speech.create(
            model="tts-1",
            voice="onyx",  # Options: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'
            input=text
        )

        # Save the response as an audio file
        audio_path = "chatgpt_voice_output.mp3"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(response.content)  # Updated to response.content

        # Load and play the audio
        audio = AudioSegment.from_file(audio_path, format="mp3")
        play(audio)

        print("[INFO] Speech played successfully.")

    except Exception as e:
        print(f"[ERROR] Failed to generate speech: {e}")

# --------------------------------------------------------------------------
# 5. Main Function
# --------------------------------------------------------------------------
def main():
    print("[INFO] Automatically summarizing all text in the active window...")

    # Automatically select and copy all text
    selected_text = get_selected_text()

    if selected_text:
        print("[DEBUG] Selected Text:", selected_text[:200])  # Print a sample of the text
        summary = summarize_with_gpt(selected_text, target_sentences=4)  # Uses GPT-4
        print("\n[SUMMARY]:")
        print(summary)
        speak_text(summary)  # Uses ChatGPT Voice
    else:
        print("[INFO] No text selected or copied.")

if __name__ == "__main__":
    main()
