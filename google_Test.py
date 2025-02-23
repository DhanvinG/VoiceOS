import pyautogui
import time
import webbrowser

def locate_and_click(image_path, confidence=0.2, pause=1.0):
    """
    Locates 'image_path' on screen at the given confidence.
    If found, clicks its center and pauses for 'pause' seconds.
    Returns True if found & clicked, otherwise False.
    """
    print(f"[INFO] Looking for {image_path}...")
    found = pyautogui.locateOnScreen(image_path, confidence=confidence)
    if found:
        center = pyautogui.center(found)
        pyautogui.click(center)
        print(f"[INFO] Clicked {image_path}")
        time.sleep(pause)
        return True
    else:
        print(f"[WARNING] {image_path} not found on screen.")
        return False

def go_to_google(query):
    """
    1) Opens google.com in default browser,
    2) Types 'query', presses Enter.
    """
    print("[INFO] Opening google.com in default browser...")
    webbrowser.open("https://www.google.com")
    time.sleep(3)  # Wait for Google to load

    # Optionally, you could click the search box or press Tab to focus it.
    # For a quick approach, we assume the cursor is in the search box or we do a coordinate click:
    # pyautogui.click(x=400, y=300)  # Adjust coords for your screen
    # time.sleep(1)

    print(f"[INFO] Typing query: {query}")
    pyautogui.typewrite(query, interval=0.05)
    pyautogui.press("enter")
    time.sleep(3)  # Wait for results to load

def go_to_images():
    """
    Click the googleimages_button.png to go to Images tab.
    """
    if locate_and_click("googleimages_button.png", confidence=0.8, pause=2.0):
        print("[INFO] Now on Images tab.")
    else:
        print("[WARNING] Could not switch to Images.")

def go_to_videos():
    """
    Click the googlevideos_button.png to go to Videos tab.
    """
    if locate_and_click("googlevideos_button.png", confidence=0.8, pause=2.0):
        print("[INFO] Now on Videos tab.")
    else:
        print("[WARNING] Could not switch to Videos.")

def go_to_news():
    """
    Click the googlenews_button.png to go to 'Shopping' tab (as you've repurposed it).
    """
    if locate_and_click("googlenews_button.png", confidence=0.8, pause=2.0):
        print("[INFO] Now on Shopping tab (mapped to News button).")
    else:
        print("[WARNING] Could not switch to Shopping.")

def go_to_shopping():
    """
    Click the googlenews_button.png to go to 'Shopping' tab (as you've repurposed it).
    """
    if locate_and_click("googleshoppings_button.png", confidence=0.8, pause=2.0):
        print("[INFO] Now on Shopping tab (mapped to News button).")
    else:
        print("[WARNING] Could not switch to Shopping.")

def test_google_search_nav():
    """
    Tests:
    1) Go to a query
    2) Click Images
    3) Click Videos
    4) Click News (Shopping)
    """
    # For demonstration, let's search "puppies"
    query = "puppies"
    go_to_google(query)

    go_to_images()
    go_to_videos()
    go_to_news()
    go_to_shopping()

    print("[INFO] Test complete. Check your browser to see if tabs switched.")

def main():
    input("[PROMPT] Ensure googleimages_button.png, googlevideos_button.png, and googlenews_button.png are present. Press Enter to continue...")
    test_google_search_nav()

if __name__ == "__main__":
    main()
