import pyautogui
import time
import webbrowser
import random

# -----------------------------
# 1. Define Greetings and Closings
# -----------------------------

GREETINGS = [
    "Dear {recipient_name},",
    "Hi {recipient_name},",
    "Hello {recipient_name},",
    "Greetings {recipient_name},",
    "Good day {recipient_name},",
    "Hey {recipient_name},",
    "Hi there {recipient_name},",
    "Dear Mr./Ms. {recipient_last_name},",
    "To {recipient_name},",
    "Hello {recipient_name},"
]

CLOSINGS = [
    "Best regards,\n{sender_name}",
    "Sincerely,\n{sender_name}",
    "Kind regards,\n{sender_name}",
    "Warm regards,\n{sender_name}",
    "Thank you,\n{sender_name}",
    "Yours faithfully,\n{sender_name}",
    "With appreciation,\n{sender_name}",
    "Best wishes,\n{sender_name}",
    "Respectfully,\n{sender_name}",
    "Cheers,\n{sender_name}"
]

# -----------------------------
# 2. Email Automation Functions
# -----------------------------

def open_gmail():
    """
    Opens Gmail in the default web browser.
    """
    print("[INFO] Opening Gmail...")
    webbrowser.open("https://mail.google.com")
    time.sleep(5)  # Adjust for your connection speed and load times.

def compose_email():
    """
    Clicks the 'Compose' button in Gmail.
    """
    print("[INFO] Clicking 'Compose' button...")
    button_location = pyautogui.locateOnScreen('compose_button.png', confidence=0.8)

    if button_location:
        print("[INFO] Compose button found!")
        button_center = pyautogui.center(button_location)
        pyautogui.click(button_center)
        time.sleep(2)
    else:
        print("[WARNING] Compose button not found on screen.")

def to_as(recipient_email):
    """
    Types the recipient's email address into the 'To' field.
    """
    print(f"[INFO] Typing recipient: {recipient_email}")
    pyautogui.typewrite(recipient_email)
    pyautogui.press('enter')
    time.sleep(1)

def subject_as(subject_text):
    """
    Types the subject text into the 'Subject' field with the first letter capitalized.
    """
    # Capitalize the first letter and make the rest lowercase
    subject_text = subject_text.capitalize()
    
    print(f"[INFO] Typing subject: {subject_text}")
    pyautogui.press('tab')
    pyautogui.typewrite(subject_text)
    time.sleep(1)

def body_as(email_body):
    """
    Types the full email body into the email body field.
    Assumes the body is already formatted with greetings and closing.
    """
    print("[INFO] Typing body...")
    pyautogui.press('tab')  # Move focus to the body field
    pyautogui.typewrite(email_body)
    time.sleep(1)


def send_email():
    """
    Sends the email by pressing Ctrl+Enter.
    """
    print("[INFO] Sending email...")
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(1)

# -----------------------------
# 3. Helper Functions for Email Body
# -----------------------------

def select_greeting(recipient_name, recipient_last_name):
    """
    Selects a random greeting.
    """
    greeting_template = random.choice(GREETINGS)
    if "{recipient_last_name}" in greeting_template and recipient_last_name:
        return greeting_template.format(recipient_last_name=recipient_last_name)
    else:
        return greeting_template.format(recipient_name=recipient_name)

def select_closing(sender_name):
    """
    Selects a random closing.
    """
    closing_template = random.choice(CLOSINGS)
    return closing_template.format(sender_name=sender_name)

def get_recipient_last_name(full_name):
    """
    Extracts the last name from the full name.
    """
    parts = full_name.strip().split()
    return parts[-1] if len(parts) > 1 else ""

def assemble_email_body(details):
    """
    Assembles the full email body.
    Ensures the body starts with a capital letter.
    """
    greeting = select_greeting(details["recipient_name"], details["recipient_last_name"])
    closing = select_closing(details["sender_name"])
    
    # Ensure the body starts with a capital letter
    main_body = details['body'].strip()
    if main_body:
        main_body = main_body[0].upper() + main_body[1:]  # Capitalize the first letter
    
    body = f"{greeting}\n\n{main_body}\n\n{closing}"
    return body


# -----------------------------
# 4. Main Function to Automate Email
# -----------------------------

def automated_email(recipient_name, recipient_email, sender_name, subject, body):
    """
    Automates the process of sending an email via Gmail.
    """
    recipient_last_name = get_recipient_last_name(recipient_name)
    email_body = assemble_email_body({
        "recipient_name": recipient_name,
        "recipient_last_name": recipient_last_name,
        "sender_name": sender_name,
        "body": body
    })

    open_gmail()
    compose_email()
    to_as(recipient_email)
    subject_as(subject)
    body_as(email_body)
    send_email()
    print("[INFO] Email sent successfully!")

# -----------------------------
# 5. Example Usage
# -----------------------------

if __name__ == "__main__":
    recipient_name = "John Doe"
    recipient_email = "johndoe@example.com"
    sender_name = "Jane Smith"
    subject = "Meeting Update"
    body = "i hope this email finds you well. I wanted to discuss the latest updates regarding our project."

    automated_email(recipient_name, recipient_email, sender_name, subject, body)
