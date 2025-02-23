import os
import re
import time
import random
import openai
import pyautogui
import pyperclip
import keyboard
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from pydub import AudioSegment
from pydub.playback import play
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from transformers import pipeline, BartTokenizer

# --------------------------------------------------------------------------
# 1. Environment Configuration
# --------------------------------------------------------------------------
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs

# Set OpenAI API Key

openai.api_key = yourapi

# Initialize tokenizer for text splitting
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

# --------------------------------------------------------------------------
# 2. Utility Functions
# --------------------------------------------------------------------------

def copy_current_url():
    """Copies the current URL from the browser."""
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'l')  # Focus address bar
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')  # Copy the URL
    time.sleep(0.3)
    url = pyperclip.paste()
    print(f"[DEBUG] Copied URL: {url}")
    return url

def fetch_page_text_requests(url):
    """Fetches visible text from a webpage using requests."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        text = soup.get_text(separator=" ").strip()
        return clean_text(text) if text else None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch content with requests: {e}")
        return None

def fetch_page_text_selenium(url):
    """Fetches visible text from a webpage using Selenium for dynamic content."""
    try:
        print("[INFO] Fetching page text using Selenium...")

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(3)

        print("[DEBUG] Page loaded successfully.")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        text = soup.get_text(separator=" ").strip()
        return clean_text(text) if text else None
    except Exception as e:
        print(f"[ERROR] Selenium failed: {e}")
        return None

def clean_text(text):
    """Cleans text by removing excessive whitespace and non-printable characters."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

# --------------------------------------------------------------------------
# 3. GPT-4 Summarization
# --------------------------------------------------------------------------

def summarize_with_gpt(text, target_sentences=4):
    """Uses GPT-4 to summarize the given text."""
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
        print("[INFO] Summary generated successfully.")
        return summary
    except Exception as e:
        print(f"[ERROR] GPT-4 summarization failed: {e}")
        return "[INFO] Unable to summarize the text."

# --------------------------------------------------------------------------
# 4. OpenAI ChatGPT Voice TTS
# --------------------------------------------------------------------------

def speak_text(text):
    """Uses OpenAI's text-to-speech API to read the text aloud using ChatGPT's voice."""
    try:
        print("[INFO] Generating speech with ChatGPT Voice...")

        response = openai.audio.speech.create(
            model="tts-1",
            voice="onyx",  # Options: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'
            input=text
        )

        # Save the response as an audio file
        audio_path = "chatgpt_voice_output.mp3"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(response.content)  # Fix: Correctly retrieve audio content

        print("[INFO] Playing the audio...")
        audio = AudioSegment.from_file(audio_path, format="mp3")
        play(audio)

        print("[INFO] Speech played successfully.")

    except Exception as e:
        print(f"[ERROR] Failed to generate speech: {e}")

# --------------------------------------------------------------------------
# 5. Main Loop Function
# --------------------------------------------------------------------------

def main_loop():
    """
    Waits for the user to press SPACE. When pressed, it copies the current
    browser URL, fetches the page content, summarizes it, and speaks the result.
    Press ESC to exit.
    """
    print("[INFO] Press SPACE to summarize the currently active page's URL.")
    print("[INFO] Press ESC to quit.")

    while True:
        if keyboard.is_pressed("space"):
            print("[INFO] Extracting URL...")
            url = copy_current_url()
            print(f"[INFO] Copied URL: {url}")

            if url:
                page_text = fetch_page_text_requests(url)

                # If insufficient text, try with Selenium
                if not page_text or len(page_text.split()) < 100:
                    print("[INFO] Trying Selenium...")
                    page_text = fetch_page_text_selenium(url)

                if page_text:
                    summary = summarize_with_gpt(page_text, target_sentences=4)
                    print("\n[SUMMARY]:")
                    print(summary)
                    speak_text(summary)
                else:
                    print("[INFO] No text available or fetch error.")
            else:
                print("[INFO] Could not copy URL. Make sure the browser is in focus.")

            time.sleep(1)

        if keyboard.is_pressed("esc"):
            print("[INFO] Exiting...")
            break

        time.sleep(0.1)  # Prevent high CPU usage

# --------------------------------------------------------------------------
# 6. Entry Point
# --------------------------------------------------------------------------

def main():
    """Entry point for the script."""
    print("[INFO] Script started successfully. Waiting for user input...")
    main_loop()

if __name__ == "__main__":
    main()
