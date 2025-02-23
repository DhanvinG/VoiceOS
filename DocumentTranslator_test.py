import re
import time
from langdetect import detect
from transformers import MarianMTModel, MarianTokenizer
import pyautogui
import pyperclip

def clean_text(text):
    """
    Cleans the text by removing non-printable characters and excessive whitespace.
    """
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def detect_language(text):
    """
    Detects the language of the input text.
    """
    try:
        language = detect(text)
        print(f"[INFO] Detected Language: {language}")
        return language
    except Exception as e:
        print(f"[ERROR] Language detection failed: {e}")
        return None

def translate_to_english(text, source_lang):
    """
    Translates text from the detected language to English.
    """
    try:
        # Use MarianMT for translation with dynamically selected model
        model_name = f"Helsinki-NLP/opus-mt-{source_lang}-en"
        tokenizer = MarianTokenizer.from_pretrained(model_name, cache_dir="./custom_cache")
        model = MarianMTModel.from_pretrained(model_name, cache_dir="./custom_cache")

        # Tokenize and translate
        inputs = tokenizer(text, return_tensors="pt", truncation=True)
        translated = model.generate(**inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

        print(f"[INFO] Translated Text: {translated_text}")
        return translated_text
    except Exception as e:
        print(f"[ERROR] Translation failed: {e}")
        return None

def select_and_copy_text():
    """
    Simulates Ctrl+A and Ctrl+C to select and copy all text in the current window.
    """
    time.sleep(0.3)  # Allow time for the active window to stabilize
    pyautogui.hotkey('ctrl', 'a')  # Select all text
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')  # Copy the selected text
    time.sleep(0.3)
    return pyperclip.paste()  # Retrieve the copied text

def replace_text_with_translation(translated_text):
    """
    Deletes the current text and replaces it with the translated text.
    """
    pyautogui.hotkey('ctrl', 'a')  # Select all text
    time.sleep(0.3)
    pyautogui.hotkey('del')  # Delete the selected text
    time.sleep(0.3)
    pyperclip.copy(translated_text)  # Copy the translated text to clipboard
    pyautogui.hotkey('ctrl', 'v')  # Paste the translated text

def process_and_replace_text():
    """
    Selects, translates, and replaces text in an external application.
    """
    original_text = select_and_copy_text()
    if original_text:
        cleaned_text = clean_text(original_text)
        detected_lang = detect_language(cleaned_text)

        if detected_lang and detected_lang != 'en':
            translated_text = translate_to_english(cleaned_text, detected_lang)
            if translated_text:
                replace_text_with_translation(translated_text)
                print("[INFO] Text replaced with translated version.")
            else:
                print("[ERROR] Translation failed.")
        elif detected_lang == 'en':
            print("[INFO] Text is already in English. No changes made.")
        else:
            print("[INFO] Unable to detect or translate the text.")
    else:
        print("[INFO] No text found or copied.")

# Entry Point
if __name__ == "__main__":
    print("[INFO] Activating translation tool...")
    print("[INFO] Ensure the target application is in focus.")
    process_and_replace_text()
