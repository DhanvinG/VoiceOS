# current

import os
import re
import time
import random
import torch
import nltk
import pyttsx3
import pyautogui
import pyperclip
import keyboard
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from transformers import pipeline
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from transformers import BartTokenizer

# --------------------------------------------------------------------------
# 1. Environment Configuration
# --------------------------------------------------------------------------
# Enable synchronous CUDA error reporting and suppress TensorFlow logs
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'  # Enables synchronous error reporting
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppresses TensorFlow logs
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disables oneDNN optimizations

# --------------------------------------------------------------------------
# 2. Initialization
# --------------------------------------------------------------------------
# Initialize the tokenizer
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

# Initialize the TTS engine using pyttsx3
tts_engine = pyttsx3.init()

def configure_tts(rate=150, volume=1.0, voice_id=None):
    """
    Configures the TTS engine's speech rate, volume, and voice.
    """
    try:
        tts_engine.setProperty('rate', rate)
        tts_engine.setProperty('volume', volume)
        if voice_id:
            tts_engine.setProperty('voice', voice_id)
    except Exception as e:
        print(f"[ERROR] Failed to configure TTS properties. Error: {e}")

def set_voice():
    """
    Sets the voice to Microsoft Zira Desktop if available.
    """
    voices = tts_engine.getProperty('voices')
    for voice in voices:
        if "Microsoft Zira Desktop" in voice.name:
            tts_engine.setProperty('voice', voice.id)
            print("Voice set to Microsoft Zira Desktop.")
            return
    print("[WARNING] Microsoft Zira Desktop voice not found. Using default voice.")

# Ensure NLTK 'punkt' is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# --------------------------------------------------------------------------
# 3. Utility Functions
# --------------------------------------------------------------------------
def copy_current_url():
    """
    Uses PyAutoGUI to highlight the browser address bar (Ctrl+L),
    copy the URL (Ctrl+C), and returns the copied URL.
    Assumes the browser window is active and in focus.
    """
    time.sleep(0.3)  # Slight delay to ensure correct timing

    # Press Ctrl+L to focus address bar (common in Chrome/Firefox)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.3)

    # Copy the highlighted address bar text
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)

    # Retrieve the text from the clipboard
    url = pyperclip.paste()
    return url

def fetch_page_text_requests(url):
    """
    Fetches all visible text from the webpage using requests.
    Suitable for static pages.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Get the visible text
        text = soup.get_text(separator=" ").strip()
        if text:
            cleaned_text = clean_text(text)
            word_count = len(cleaned_text.split())
            sentence_count = len(sent_tokenize(cleaned_text))
            sample = text_sample(cleaned_text, 200)
            print(f"[DEBUG] Fetched text length (requests): {word_count} words")
            print(f"[DEBUG] Number of sentences: {sentence_count}")
            print(f"[DEBUG] Sample text:\n{sample}\n")
            return cleaned_text
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch content with requests: {e}")
        return None

def fetch_page_text_selenium(url):
    """
    Fetches all visible text from the webpage using Selenium.
    Handles dynamic content rendering.
    """
    try:
        # Initialize Selenium WebDriver with Chrome in headless mode
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--disable-gpu')  # Disable GPU (Windows specific)
        options.add_argument('--no-sandbox')  # Bypass OS security model
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Navigate to the URL
        driver.get(url)

        # Wait for the page to fully load (adjust as needed)
        time.sleep(3)

        # Extract page source after JavaScript has rendered
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Get the visible text
        text = soup.get_text(separator=" ").strip()
        if text:
            cleaned_text = clean_text(text)
            word_count = len(cleaned_text.split())
            sentence_count = len(sent_tokenize(cleaned_text))
            sample = text_sample(cleaned_text, 200)
            print(f"[DEBUG] Fetched text length (Selenium): {word_count} words")
            print(f"[DEBUG] Number of sentences: {sentence_count}")
            print(f"[DEBUG] Sample text:\n{sample}\n")
            driver.quit()
            return cleaned_text
        else:
            driver.quit()
            return None
    except Exception as e:
        print(f"[ERROR] Selenium failed to fetch content: {e}")
        return None

def clean_text(text):
    """
    Cleans the text by removing non-printable characters and excessive whitespace.
    """
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def split_text_by_tokens(text, max_tokens=800):
    """
    Splits the text into chunks based on token counts without breaking sentences.

    Args:
        text (str): The full text to split.
        max_tokens (int): Maximum number of tokens per chunk.

    Returns:
        list: A list of text chunks.
    """
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
                # If a single sentence exceeds max_tokens, split the sentence
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

def split_text(text, max_tokens=800):
    """
    Wrapper function to split text using token-based splitting.

    **Updated to accept 'max_tokens' instead of 'max_length' to match function calls.**
    """
    return split_text_by_tokens(text, max_tokens=max_tokens)

def text_sample(text, max_length=200):
    """
    Returns a sample of the text up to max_length characters.
    """
    return text[:max_length] + ("..." if len(text) > max_length else "")

def make_conversational(summary, target_sentences=4):
    """
    Transforms the summary into a more conversational and user-friendly tone.
    Adds a random introductory phrase.
    """
    intro_phrases = [
        "Sure! Here's what I found about the site:",
        "Let me explain what I found:",
        "Here's a quick summary of what I learned:",
        "Okay! Here's what the page is about:"
    ]
    intro = random.choice(intro_phrases)

    sentences = sent_tokenize(summary)
    trimmed_sentences = sentences[:target_sentences]
    conversational_sentences = [intro] + trimmed_sentences
    return ' '.join(conversational_sentences)

def explain_text(text, batch_size=8, target_sentences=4, max_tokens=160, min_tokens=120):
    """
    Summarizes the content of the text, processes it, and makes it conversational.
    """
    try:
        # Initialize the summarizer pipeline
        summarizer = pipeline(
            "summarization", 
            model="facebook/bart-large-cnn", 
            framework="pt", 
            device=0 if torch.cuda.is_available() else -1
        )

        device = "cuda:0" if torch.cuda.is_available() else "CPU"
        print(f"Device set to use {device}")

        # Split text based on token counts
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

        conversational_summary = make_conversational(trimmed_summary, target_sentences)

        # Speak the summary aloud
        speak_text(conversational_summary)

        return conversational_summary
    except Exception as e:
        print(f"[ERROR] Summarization failed: {e}")
        return "[INFO] Unable to explain the text."

def speak_text(text):
    """
    Speaks the text using Microsoft Zira Desktop voice via pyttsx3.
    """
    try:
        set_voice()
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"[ERROR] Failed to speak text. Error: {e}")

# --------------------------------------------------------------------------
# 4. Main Loop Function
# --------------------------------------------------------------------------
def main_loop():
    """
    Waits for the space bar. 
    When pressed, copies the current browser URL, fetches the page content,
    summarizes it, and speaks the result.
    Press ESC to exit.
    """
    print("[INFO] Make sure your browser is in focus and on the page you want.")
    print("[INFO] Press SPACE to summarize the currently active page's URL.")
    print("[INFO] Press ESC to quit.")

    while True:
        # If the user presses space, copy the URL and summarize
        if (1 == 1):
            print("Extracting URL...")
            url = copy_current_url()
            print(f"[INFO] Copied URL: {url}")

            if url:
                # First, try fetching with requests
                page_text = fetch_page_text_requests(url)

                # If insufficient text, try with Selenium
                if not page_text or len(page_text.split()) < 100:
                    print("[INFO] The page might have dynamic content. Trying Selenium...")
                    page_text = fetch_page_text_selenium(url)

                if page_text:
                    explanation = explain_text(
                        page_text, 
                        batch_size=8, 
                        target_sentences=4, 
                        max_tokens=160, 
                        min_tokens=120
                    )
                    print("\n[EXPLANATION]:")
                    print(explanation)
                else:
                    print("[INFO] No text available or fetch error.")
            else:
                print("[INFO] Could not copy URL. Make sure the browser address bar is accessible.")

            # Add a small delay so it doesn't register multiple presses at once
            time.sleep(1)

        # If the user presses ESC, break out of the loop
        if keyboard.is_pressed("esc"):
            print("[INFO] Exiting...")
            break

        time.sleep(0.1)  # Sleep briefly to prevent high CPU usage in the loop

# --------------------------------------------------------------------------
# 5. Entry Point
# --------------------------------------------------------------------------
def main():
    """
    Entry point for the script.
    """
    main_loop()

if __name__ == "__main__":
    # Optional: configure TTS settings if you like
    # configure_tts(rate=160, volume=0.9)

    set_voice()  # Set the desired voice at the start
    main()
