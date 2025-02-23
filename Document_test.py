import pyautogui
import time
import webbrowser

# ------------------------------------------------------------------------------
# Helper Functions: Locating & Clicking Images
# ------------------------------------------------------------------------------

def locate_and_click(image_path, confidence=0.8, pause=1.0):
    """
    Searches the screen for 'image_path' (PNG) at 'confidence' level.
    If found, clicks its center and returns True.
    If not found, prints a warning and returns False.
    'pause' is how long to sleep after a successful click (to let menus load).
    """
    print(f"[INFO] Looking for {image_path}...")
    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
    if location:
        center = pyautogui.center(location)
        pyautogui.click(center)
        print(f"[INFO] Clicked {image_path}")
        time.sleep(pause)
        return True
    else:
        print(f"[WARNING] {image_path} not found on screen.")
        return False

# ------------------------------------------------------------------------------
# Google Docs Basic Operations
# ------------------------------------------------------------------------------

def open_new_doc():
    """
    Opens a new blank Google Doc using docs.new in the default browser.
    """
    print("[INFO] Opening a new Google Doc...")
    webbrowser.open("https://docs.new")
    time.sleep(5)  # Adjust for your system/network

def set_doc_title(title):
    """
    Clicks the doc's title bar, types a new title, and presses Enter.
    Using coordinate-based click. Update (x=...) to match your screen.
    """
    print(f"[INFO] Setting doc title to: {title}")
    pyautogui.click(x=100, y=100)  # <-- Replace with your title bar coords
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')  # Windows/Linux. On Mac, use ('command', 'a')
    time.sleep(0.5)
    pyautogui.typewrite(title)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1)

def type_sample_text(text):
    """
    Types sample text into the main doc body.
    Update (x=500, y=500) if needed to ensure cursor is in the doc body.
    """
    print("[INFO] Typing sample text...")
    pyautogui.click(x=500, y=500)  
    time.sleep(1)
    pyautogui.typewrite(text, interval=0.05)

def select_all():
    print("[INFO] Selecting all text...")
    pyautogui.hotkey('ctrl', 'a')  # Mac: ('command', 'a')
    time.sleep(0.5)

def bold_text():
    print("[INFO] Bold formatting...")
    pyautogui.hotkey('ctrl', 'b')  # Mac: ('command', 'b')
    time.sleep(0.5)

def underline_text():
    print("[INFO] Underline formatting...")
    pyautogui.hotkey('ctrl', 'u')  # Mac: ('command', 'u')
    time.sleep(0.5)

def italicize_text():
    print("[INFO] Italicize formatting...")
    pyautogui.hotkey('ctrl', 'i')  # Mac: ('command', 'i')
    time.sleep(0.5)

def share_document(email):
    """
    Clicks the 'Share' button (coordinate-based), types an email, presses Enter.
    If you have 'done_button.png', tries to locate & click it.
    """
    print("[INFO] Sharing document...")
    pyautogui.click(x=1750, y=100)  # Replace with your 'Share' button coords
    time.sleep(3)

    pyautogui.click(x=1000, y=450)  # Replace with the text field in share dialog
    time.sleep(1)
    pyautogui.typewrite(email)
    time.sleep(1)

    pyautogui.press('enter')
    time.sleep(1)

    # If you want to click a 'Done' button image:
    done_btn = pyautogui.locateOnScreen('done_button.png', confidence=0.8)
    if done_btn:
        print("[INFO] Done button found, clicking it.")
        pyautogui.click(pyautogui.center(done_btn))

    time.sleep(2)
    print("[INFO] Document shared.")

# ------------------------------------------------------------------------------
# Download Functions (Uses image-based approach)
# ------------------------------------------------------------------------------

def download_as_pdf():
    """
    1) Clicks 'File' (file_button.png)
    2) Clicks 'Download' (download_button.png)
    3) Clicks 'PDF' (pdf_button.png)
    """
    print("[INFO] Downloading as PDF...")
    # 1. File menu
    if not locate_and_click('file_button.png', pause=1.5):
        return
    # 2. Download submenu
    if not locate_and_click('download_button.png', pause=1.5):
        return
    # 3. PDF option
    if not locate_and_click('pdf_button.png', pause=2.0):
        return
    print("[INFO] PDF download initiated. Check your downloads folder.")

def download_as_word():
    """
    1) Clicks 'File' (file_button.png)
    2) Clicks 'Download' (download_button.png)
    3) Clicks 'Word' (word_button.png)
    """
    print("[INFO] Downloading as Word (.docx)...")
    # 1. File menu
    if not locate_and_click('file_button.png', pause=1.5):
        return
    # 2. Download submenu
    if not locate_and_click('download_button.png', pause=1.5):
        return
    # 3. Word option
    if not locate_and_click('word_button.png', pause=2.0):
        return
    print("[INFO] Word download initiated. Check your downloads folder.")

# ------------------------------------------------------------------------------
# Main Demo
# ------------------------------------------------------------------------------

def main():
    """
    1) Open a new doc
    2) Set title
    3) Type sample text
    4) Format (select all, bold, underline, italic)
    5) Share doc
    6) Download as PDF / Word
    """
    input("[PROMPT] Make sure you're logged into Google. Press Enter to start...")

    # Basic doc workflow
    open_new_doc()
    set_doc_title("My Automated PyAutoGUI Doc")
    type_sample_text("Hello, this text is typed by PyAutoGUI!\nFeel free to edit or remove it.")
    select_all()
    bold_text()
    underline_text()
    italicize_text()

    # Share the doc
    share_document("gdhanvin9@gmail.com")

    # Optionally, download as PDF or Word
    download_as_pdf()

    # input("[PROMPT] Press Enter to try Download as Word...")
    # download_as_word()

    print("[INFO] Script finished. Check your doc & downloads folder.")

if __name__ == "__main__":
    main()
