import pyautogui
import time
import webbrowser

def locate_and_click(image_path, confidence=0.8, pause=1.0):
    """Locate an image on the screen and click it."""
    print(f"[INFO] Looking for {image_path}...")
    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
    if location:
        pyautogui.click(pyautogui.center(location))
        print(f"[INFO] Clicked on {image_path}.")
        time.sleep(pause)
        return True
    else:
        print(f"[WARNING] {image_path} not found.")
        return False

def send_email_via_google_meet(email_address):
    """Automates the process of sending an invite email via Google Meet."""
    google_meet_link = "https://meet.google.com/getalink?authuser=0&illm=1735328973837&hl=en&hs=203"
    print("[INFO] Opening Google Meet link...")
    webbrowser.open(google_meet_link)
    time.sleep(3)  # Wait for the page to load
    
    if not locate_and_click('sendinvite_button.png', pause=2.0):
        print("[ERROR] Failed to click 'Send Invite' button.")
        return
    if not locate_and_click('shareemail_button.png', pause=2.0):
        print("[ERROR] Failed to click 'Share Email' button.")
        return
    
    print(f"[INFO] Typing email address: {email_address}")
    pyautogui.typewrite(email_address)
    time.sleep(1)
    
    if not locate_and_click('send_button.png', pause=2.0):
        print("[ERROR] Failed to click 'Send' button.")
        return

    print("[INFO] Invite email sent successfully!")

# Ensure the script only runs the following block if executed directly
if __name__ == "__main__":
    send_email_via_google_meet("example@example.com")
