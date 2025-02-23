import pyautogui
import tkinter as tk
import threading
import time
import subprocess
import sys
import os
# import speech_recognition as sr  # <-- comment this out
import openai

def transcribe_audio(filename):
    """Transcribes an audio file using OpenAI Whisper API."""
    with open(filename, "rb") as audio_file:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text.strip()


import sounddevice as sd
import numpy as np
import wave

from tkinter import ttk, messagebox, PhotoImage, font as tkfont

# ------------------- ALL YOUR CUSTOM IMPORTS -------------------
from vscode_testing import open_vscode, create_file, save_file, run_file
from google_Test import go_to_google, go_to_images, go_to_videos, go_to_news, go_to_shopping
from mailsend_test import send_email_via_google_meet
from email_test import (
    open_gmail,
    compose_email,
    to_as,
    subject_as,
    body_as,
    send_email,
    automated_email,
    get_recipient_last_name,
    assemble_email_body
)
from Document_test import (
    open_new_doc,
    set_doc_title,
    type_sample_text,
    select_all,
    bold_text,
    underline_text,
    italicize_text,
    share_document,
    download_as_pdf,
    download_as_word
)
from shortcuts_test import (
    bookmark,
    refresh,
    back,
    forward,
    snap_left,
    snap_right,
    switch_window,
    maximize,
    minimize,
    close_window,
    undo,
    redo,
    cut,
    copy,
    paste
)



# ---------------------------------------------------------------

# ---------------------- GLOBAL VARIABLES -----------------------
root = None        # Will hold the main Tkinter window
text_display = None  # Will reference the text box in create_gui()

email_mappings = {
    "john": "john@gmail.com",
    "jane": "jane@example.com",
    "joe": "doe@example.com",
    "dhanvitha": "dhanvithag2012@gmail.com",
}

email_details = {
    "recipient_name": None,
    "recipient_email": None,
    "sender_name": "Dhanvin",
    "subject": None,
    "body": None
}
# ---------------------------------------------------------------

COMMAND_MAPPINGS = {
    "new document": "open_new_doc()",
    "title as": "set_doc_title('{arg}')",
    "type": "type_sample_text('{arg}')",
    "select all": "select_all()",
    "bold": "bold_text()",
    "underline": "underline_text()",
    "italicize": "italicize_text()",
    "search": "go_to_google('{arg}')",
    "open code": "open_vscode()",
    "save file": "save_file()",
    "run file": "run_file()",
    "send mail": "send_email()",
    "exit": "sys.exit(0)",
    "compose to": "compose_email(); to_as('{arg}')",
    "subject as": "subject_as('{arg}')",
    "body as": "body_as('{arg}')",
    "meet invite to": "send_email_via_google_meet('{arg}')",
    "bookmark as": "bookmark('{arg}')",
    "close": "pyautogui.hotkey('ctrl', 'w')",
    "reopen": "pyautogui.hotkey('ctrl', 'shift', 't')",
    "refresh": "refresh()",
    "back": "back()",
    "forward": "forward()",
    "snap left": "snap_left()",
    "snap right": "snap_right()",
    "switch window": "switch_window()",
    "maximize": "maximize()",
    "minimize": "minimize()",
    "close window": "close_window()",
    "undo": "undo()",
    "redo": "redo()",
    "cut": "cut()",
    "copy": "copy()",
    "paste": "paste()",
}



def ensure_text_box_focus():
    """Ensure the text box remains focused."""
    while True:
        time.sleep(0.2)
        if text_display is not None:
            if text_display.focus_get() != text_display:
                text_display.focus_force()

def clear_text_box():
    """Clear all text in the text box."""
    if text_display is not None:
        text_display.delete("1.0", tk.END)

def monitor_text_for_commands():
    """Continuously monitor the text box for commands and run them."""
    last_processed_command = None

    while True:
        time.sleep(0.5)
        if text_display is None:
            continue

        text = text_display.get("1.0", tk.END).strip().lower()
        if not text:
            last_processed_command = None
            continue

        if text == last_processed_command:
            continue

        last_processed_command = text

        # --------------- EXAMPLES OF COMMAND HANDLING ---------------

        # Google Docs-related commands
        if text.startswith("new document"):
            open_new_doc()
            clear_text_box()

        elif text.startswith("title as"):
            title = text.replace("title as", "").strip().capitalize()
            set_doc_title(title)
            clear_text_box()

        elif text.startswith("type"):
            content = text.replace("type", "").strip()
            type_sample_text(content)
            clear_text_box()

        elif text.startswith("select all"):
            select_all()
            clear_text_box()

        elif text.startswith("bold"):
            bold_text()
            clear_text_box()

        elif text.startswith("underline"):
            underline_text()
            clear_text_box()

        elif text.startswith("italicize"):
            italicize_text()
            clear_text_box()

        elif text.startswith("share to"):
            recipient_name = text.replace("share to", "").strip()
            if recipient_name in email_mappings:
                share_document(email_mappings[recipient_name])
            clear_text_box()

        elif text.startswith("download as pdf"):
            download_as_pdf()
            clear_text_box()

        elif text.startswith("download as word"):
            download_as_word()
            clear_text_box()

        # Email-related commands
        elif text == "open mail":
            open_gmail()
            clear_text_box()

        elif text.startswith("compose to"):
            recipient_name = text.replace("compose to", "").strip()
            if recipient_name in email_mappings:
                email_details["recipient_name"] = recipient_name
                email_details["recipient_email"] = email_mappings[recipient_name]
                compose_email()
                to_as(email_details["recipient_email"])
            clear_text_box()

        elif text.startswith("subject as"):
            subject = text.replace("subject as", "").strip()
            email_details["subject"] = subject
            subject_as(subject)
            clear_text_box()

        elif text.startswith("body as"):
            body_input = text.replace("body as", "").strip()
            if email_details["recipient_name"] and email_details["sender_name"]:
                recipient_last_name = get_recipient_last_name(email_details["recipient_name"])
                email_body = assemble_email_body({
                    "recipient_name": email_details["recipient_name"],
                    "recipient_last_name": recipient_last_name,
                    "sender_name": email_details["sender_name"],
                    "body": body_input
                })
                email_details["body"] = email_body
                body_as(email_body)
            clear_text_box()

        elif text == "send mail":
            if email_details["recipient_email"] and email_details["subject"] and email_details["body"]:
                send_email()
            clear_text_box()

        # Google search and sub-sections
        elif text.startswith("search"):
            query = text.replace("search", "").strip()
            if query:
                go_to_google(query)
            clear_text_box()

        elif "go to images" in text:
            go_to_images()
            clear_text_box()

        elif "go to videos" in text:
            go_to_videos()
            clear_text_box()

        elif "go to news" in text:
            go_to_news()
            clear_text_box()

        elif "go to shopping" in text:
            go_to_shopping()
            clear_text_box()

        # VS Code Commands
        elif "open code" in text:
            open_vscode()
            clear_text_box()

        elif "create a" in text and "file as" in text:
            file_type, file_name = parse_create_file_command(text)
            if file_type and file_name:
                create_file(file_type, file_name)
            clear_text_box()

        elif "save" in text:
            save_file()
            clear_text_box()

        elif "run" in text:
            run_file()
            clear_text_box()

        # Script execution
        elif "summarize" in text:
            execute_script_command("DocumentSummarizer_test.py")
        elif "explain" in text:
            execute_script_command("updatedvoice_test.py")
        elif "translate" in text:
            execute_script_command("DocumentTranslator_test.py")

        elif "exit" in text:
            print("Exiting the program.")
            sys.exit(0)

        # Meet invite
        elif text.startswith("meet invite to"):
            recipient = text.replace("meet invite to", "").strip()
            if recipient in email_mappings:
                send_email_via_google_meet(email_mappings[recipient])
            clear_text_box()

        # Common shortcuts
        elif text.startswith("close"):
            pyautogui.hotkey('ctrl', 'w')

        elif text.startswith("reopen"):
            pyautogui.hotkey('ctrl', 'shift', 't')

        elif text.startswith("bookmark as"):
            bookmark_name = text.replace("bookmark as", "").strip()
            if bookmark_name:
                bookmark(bookmark_name)
            clear_text_box()

        elif text == "refresh":
            refresh()
            clear_text_box()

        elif text == "back":
            back()
            clear_text_box()

        elif text == "forward":
            forward()
            clear_text_box()

        elif text == "snap left":
            snap_left()
            clear_text_box()

        elif text == "snap right":
            snap_right()
            clear_text_box()

        elif text == "switch window":
            switch_window()
            clear_text_box()

        elif text == "maximize":
            maximize()
            clear_text_box()

        elif text == "minimize":
            minimize()
            clear_text_box()

        elif text == "close window":
            close_window()
            clear_text_box()

        elif text == "undo":
            undo()
            clear_text_box()

        elif text == "redo":
            redo()
            clear_text_box()

        elif text == "cut":
            cut()
            clear_text_box()

        elif text == "copy":
            copy()
            clear_text_box()

        elif text == "paste":
            paste()
            clear_text_box()

        # Add additional commands as needed...

def parse_create_file_command(command_text):
    """Parse the file type and name from something like 'create a python file as test.py'."""
    try:
        file_type_start = command_text.index("create a") + len("create a")
        file_type_end = command_text.index("file as")
        file_type = command_text[file_type_start:file_type_end].strip()

        file_name_start = command_text.index("file as") + len("file as")
        file_name = command_text[file_name_start:].strip()

        # Map "notebook" to "jupyter notebook"
        if file_type.lower() == "notebook":
            file_type = "jupyter notebook"

        return file_type, file_name
    except ValueError:
        return None, None

def execute_script_command(script_name):
    """Launch a Python script in a new process."""
    print(f"Executing {script_name}...")
    try:
        subprocess.Popen([sys.executable, script_name])
        clear_text_box()
    except Exception as e:
        print(f"[ERROR] Failed to execute {script_name}: {e}")

# def continuous_speech_recognition():
#     """
#     Continuously capture microphone input, send it to OpenAI Whisper API only if speech is detected,
#     and update the text box with recognized text.
#     """
#     while True:
#         filename = "temp_command.wav"
#         if record_audio(filename, duration=4):  # Only proceed if speech is detected
#             try:
#                 recognized_text = transcribe_audio(filename)  # ✅ Now the function exists!
#                 if recognized_text:
#                     print(f"[INFO] Recognized: {recognized_text}")
#                     update_text_box(recognized_text)  # Update GUI text box
#             except openai.OpenAIError as e:
#                 print(f"[ERROR] OpenAI Whisper API Error: {e}")
#             except Exception as e:
#                 print(f"[ERROR] Unexpected error: {e}")

#         time.sleep(0.3)


def continuous_speech_recognition():
    while True:
        filename = "temp_command.wav"
        if record_audio(filename, duration=2):  # ✅ Shortened duration for faster response
            try:
                recognized_text = transcribe_audio(filename)
                if recognized_text:
                    print(f"[INFO] Recognized: {recognized_text}")
                    update_text_box(recognized_text)  # ✅ Update GUI
                    execute_voice_command(recognized_text)  # ✅ NEW: Execute immediately
            except openai.OpenAIError as e:
                print(f"[ERROR] OpenAI Whisper API Error: {e}")
            except Exception as e:
                print(f"[ERROR] Unexpected error: {e}")

        time.sleep(0.3)  # ✅ Shortened delay for responsiveness

def execute_voice_command(text):
    """Executes the closest matching command from COMMAND_MAPPINGS."""
    text = text.lower().strip()  # Normalize text

    for command, action in COMMAND_MAPPINGS.items():
        if text.startswith(command):  # ✅ Check for command match
            arg = text.replace(command, "").strip()  # ✅ Extract argument if exists
            print(f"[INFO] Executing command: {command} with argument: {arg}")

            try:
                if "{arg}" in action:
                    eval(action.format(arg=arg))  # ✅ Execute with argument
                else:
                    eval(action)  # ✅ Execute without argument
                clear_text_box()
                return  # ✅ Exit after executing the first match

            except Exception as e:
                print(f"[ERROR] Failed to execute {command}: {e}")
    
    print("[INFO] No matching command found.")



def record_audio(filename="temp_command.wav", duration=2, samplerate=22050):
    """
    Records 'duration' seconds of audio to 'filename' using sounddevice.
    Skips processing if no speech is detected.
    """
    import sounddevice as sd
    import numpy as np
    import wave

    print("[INFO] Recording audio...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished

    # Check if the recording contains significant sound
    if np.any(np.abs(audio_data) > 1000):  # Threshold to detect speech presence
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())
        print("[INFO] Speech detected, audio recorded.")
        return True  # Audio contains speech, proceed with Whisper
    else:
        print("[INFO] No speech detected, skipping API call.")
        return False  # Skip processing if no speech detected

def update_text_box(text):
    """Replace the text in the Tkinter text box with new recognized text."""
    if text_display is not None:
        clear_text_box()
        text_display.insert(tk.END, text + "\n")
        text_display.see(tk.END)

# ------------------- NEW SMALL-GUI CODE BEGINS HERE -------------------
def create_curved_button(canvas, x, y, width, height, radius, text, command,
                         bg_color="#0078D7", fg_color="#FFFFFF", hover_color="#005A9E"):
    """Helper to draw a custom rounded-corner button on a canvas."""
    # Draw arcs and rectangles for rounded corners
    canvas.create_arc(x, y, x + 2 * radius, y + 2 * radius, start=90, extent=90, fill=bg_color, outline="", tags="button_bg")
    canvas.create_arc(x + width - 2 * radius, y, x + width, y + 2 * radius, start=0, extent=90, fill=bg_color, outline="", tags="button_bg")
    canvas.create_arc(x + width - 2 * radius, y + height - 2 * radius, x + width, y + height, start=270, extent=90, fill=bg_color, outline="", tags="button_bg")
    canvas.create_arc(x, y + height - 2 * radius, x + 2 * radius, y + height, start=180, extent=90, fill=bg_color, outline="", tags="button_bg")
    canvas.create_rectangle(x + radius, y, x + width - radius, y + height, fill=bg_color, outline="", tags="button_bg")
    canvas.create_rectangle(x, y + radius, x + width, y + height - radius, fill=bg_color, outline="", tags="button_bg")

    # Add the button text
    button_text = canvas.create_text(x + width / 2, y + height / 2,
                                     text=text, fill=fg_color, font=("Segoe UI", 12, "bold"),
                                     tags="button_text")

    def on_enter(event):
        canvas.itemconfig("button_bg", fill=hover_color)
        canvas.itemconfig("button_text", fill=fg_color)

    def on_leave(event):
        canvas.itemconfig("button_bg", fill=bg_color)
        canvas.itemconfig("button_text", fill=fg_color)

    canvas.tag_bind("button_bg", "<Enter>", on_enter)
    canvas.tag_bind("button_text", "<Enter>", on_enter)
    canvas.tag_bind("button_bg", "<Leave>", on_leave)
    canvas.tag_bind("button_text", "<Leave>", on_leave)

    def on_click(event):
        command()

    canvas.tag_bind("button_bg", "<Button-1>", on_click)
    canvas.tag_bind("button_text", "<Button-1>", on_click)

def open_settings_image():
    """Open the settings image in full screen."""
    settings_window = tk.Toplevel(root)
    settings_window.attributes("-fullscreen", True)
    settings_window.configure(bg="#000000")

    try:
        settings_image = PhotoImage(file="settings_button.png")
        settings_label = tk.Label(settings_window, image=settings_image, bg="#000000")
        settings_label.image = settings_image
        settings_label.pack(expand=True, fill="both")

        settings_label.bind("<Button-1>", lambda e: settings_window.destroy())
    except Exception as e:
        print(f"[ERROR] Failed to load settings image: {e}")
        settings_label = tk.Label(settings_window, text="Settings Image Not Found", bg="#000000", fg="#FFFFFF", font=("Segoe UI", 24))
        settings_label.pack(expand=True, fill="both")
        settings_label.bind("<Button-1>", lambda e: settings_window.destroy())

def create_gui():
    """Create the new, smaller main GUI."""
    global root, text_display

    root = tk.Tk()
    root.title("VoiceOS")
    root.geometry("350x200")
    root.attributes("-topmost", True)
    root.resizable(False, False)
    root.configure(bg="#F0F2F5")

    text_font = tkfont.Font(family="Segoe UI", size=10)

    # Header image / logo
    try:
        logo_image = PhotoImage(file="logo_image.png")
        max_width = 500
        max_height = 112
        scale_factor = min(max_width / logo_image.width(), max_height / logo_image.height())
        new_width = int(logo_image.width() * scale_factor)
        new_height = int(logo_image.height() * scale_factor)
        resized_logo = logo_image.subsample(logo_image.width() // new_width, logo_image.height() // new_height)

        header_label = tk.Label(root, image=resized_logo, bg="#F0F2F5")
        header_label.image = resized_logo
        header_label.pack(pady=(1, 0))

        # Clicking logo opens settings
        header_label.bind("<Button-1>", lambda e: open_settings_image())
    except Exception as e:
        print(f"[ERROR] Failed to load logo image: {e}")
        header_label = tk.Label(root, text="Logo Not Found", font=("Segoe UI", 14, "bold"), bg="#F0F2F5", fg="#333333")
        header_label.pack(pady=(10, 0))

    # White text box
    text_display = tk.Text(
        root, height=6, wrap="word", font=text_font,
        bg="#FFFFFF", fg="#333333",
        bd=2, relief="groove", padx=10, pady=10
    )
    text_display.pack(padx=15, pady=(0, 10))

    # Curved-button canvas
    button_canvas = tk.Canvas(root, width=150, height=40, bg="#F0F2F5", highlightthickness=0)
    button_canvas.pack(pady=(5, 5))

    # Create the actual curved button
    create_curved_button(
        button_canvas,
        x=0,
        y=5,
        width=150,
        height=30,
        radius=15,
        text="Settings",
        command=open_settings_image,
        bg_color="#0078D7",
        fg_color="#FFFFFF",
        hover_color="#005A9E"
    )

    # Start background threads:
    threading.Thread(target=ensure_text_box_focus, daemon=True).start()
    threading.Thread(target=monitor_text_for_commands, daemon=True).start()
    threading.Thread(target=continuous_speech_recognition, daemon=True).start()

    root.mainloop()

# ------------------- SPLASH SCREEN CODE -------------------
def start_program():
    """Close the splash screen and open the main GUI."""
    splash_window.destroy()
    # After splash closes, open the smaller GUI with voice functionality
    create_gui()

splash_window = tk.Tk()
splash_window.title("Welcome to VoiceOS")
splash_window.attributes("-fullscreen", True)
splash_window.configure(bg="#121233")

try:
    image = PhotoImage(file="display_image.png")
    screen_width = splash_window.winfo_screenwidth()
    screen_height = splash_window.winfo_screenheight()
    scaled_image = image.subsample(int(image.width() / screen_width), int(image.height() / screen_height))
    image_label = tk.Label(splash_window, image=scaled_image, bg="#121233")
    image_label.pack(expand=True, fill="both")
    image_label.bind("<Button-1>", lambda e: start_program())
except Exception as e:
    print(f"[ERROR] Failed to load splash image: {e}")
    fallback_label = tk.Label(splash_window, text="Splash Image Not Found\nClick to Continue", bg="#121233", fg="#FFFFFF", font=("Segoe UI", 24))
    fallback_label.pack(expand=True, fill="both")
    fallback_label.bind("<Button-1>", lambda e: start_program())

# Before starting the splash screen, verify required scripts/images if desired:
required_scripts = ["DocumentSummarizer_test.py", "updatedvoice_test.py", "DocumentTranslator_test.py"]
missing_scripts = [script for script in required_scripts if not os.path.isfile(script)]
if missing_scripts:
    print(f"[ERROR] Missing required files: {', '.join(missing_scripts)}")
    # Optionally exit, or just warn

# Finally, start the splash screen event loop:
splash_window.mainloop()
