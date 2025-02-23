# import pyautogui
# import time

# def locate_and_click(image_path, confidence=0.8, pause=1.0):
#     """
#     1) Locate 'image_path' on screen at 'confidence'.
#     2) Click its center if found.
#     3) Pause for 'pause' seconds afterward.
#     Returns True if found & clicked, otherwise False.
#     """
#     print(f"[INFO] Looking for {image_path}...")
#     location = pyautogui.locateOnScreen(image_path, confidence=confidence)
#     if location:
#         center = pyautogui.center(location)
#         pyautogui.click(center)
#         print(f"[INFO] Clicked {image_path}")
#         time.sleep(pause)
#         return True
#     else:
#         print(f"[WARNING] {image_path} not found on screen.")
#         return False

# def automate_coding(file_type, file_name):
#     """
#     Follow the exact steps:
#     1) Click search_button.png to open Windows search.
#     2) Type 'visual studio code' + Enter to launch.
#     3) Wait, then press Win + Up to maximize.
#     4) Press Ctrl + Alt + Win + N (new file).
#     5) Type file_type (e.g., 'python', 'java', 'jupyter notebook'), press Enter.
#     6) Type file_name, then click createfile_button.png to finalize.
#     """

#     print("[INFO] Step 1: Click the Windows search button.")
#     if not locate_and_click("search_button.png", confidence=0.8, pause=1.0):
#         print("[ERROR] Could not find search_button.png. Exiting.")
#         return

#     print("[INFO] Step 2: Type 'visual studio code' and press Enter.")
#     pyautogui.typewrite("visual studio code", interval=0.05)
#     pyautogui.press("enter")
#     print("[INFO] Waiting for VS Code to open...")
#     time.sleep(5)  # Adjust if needed

#     print("[INFO] Step 3: Press Win + Up to maximize the tab.")
#     pyautogui.hotkey("win", "up")
#     time.sleep(1)

#     print("[INFO] Step 4: Press Ctrl + Alt + Win + N for a new file.")
#     pyautogui.hotkey("ctrl", "alt", "win", "n")
#     time.sleep(1)

#     print(f"[INFO] Step 5: Type the file type '{file_type}' and press Enter.")
#     pyautogui.typewrite(file_type, interval=0.05)
#     pyautogui.press("enter")
#     time.sleep(1)

#     print(f"[INFO] Step 6: Type the file name '{file_name}'.")
#     pyautogui.typewrite(file_name, interval=0.05)
#     time.sleep(1)

#     print("[INFO] Step 7: Click the createfile_button.png.")
#     if locate_and_click("createfile_button.png", confidence=0.8, pause=1.0):
#         print(f"[INFO] Created a new {file_type} file named '{file_name}'.")
#     else:
#         print("[WARNING] createfile_button.png not found. Could not finalize file creation.")

# def save_file():
#     """
#     Press Ctrl+S to save the current file in VS Code.
#     """
#     print("[INFO] Pressing Ctrl+S to save...")
#     pyautogui.hotkey("ctrl", "s")
#     time.sleep(1)  # Give it a moment to save

# def run_with_command_palette():
#     """
#     1) Press Ctrl+Shift+P to open the VS Code command palette.
#     2) Type 'command_text' (default: 'run').
#     3) Press Enter to execute that command.
    
#     Customize 'command_text' for your use case 
#     (e.g. "Python: Run Python File in Terminal").
#     """
#     if locate_and_click("run_button.png", confidence=0.8, pause=1.0):
#         print(f"running")
#     else:
#         print("[WARNING] NOT Running")
#     time.sleep(1)


# def main():
#     """
#     Example usage:
#     1) Automate coding in VS Code by creating a new Python file, 
#        saving it, and running a command palette action.
#     """
#     input("[PROMPT] Ensure 'search_button.png' and 'createfile_button.png' are present. Press Enter...")

#     # Create a Python file, for example
#     file_type = "python"
#     file_name = "example_script3.py"

#     automate_coding(file_type, file_name)

#     # Now save the file
#     save_file()

#     # Then run a command via the command palette
#     run_with_command_palette()

#     print("[INFO] Script finished. Check VS Code to see if everything worked.")

# if __name__ == "__main__":
#     main()

import pyautogui
import time
import subprocess
import sys
import os

def locate_and_click(image_path, confidence=0.8, pause=1.0):
    """
    1) Locate 'image_path' on screen with specified 'confidence'.
    2) Click its center if found.
    3) Pause for 'pause' seconds afterward.
    Returns True if found & clicked, otherwise False.
    """
    print(f"[INFO] Looking for {image_path}...")
    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
    if location:
        center = pyautogui.center(location)
        pyautogui.click(center)
        print(f"[INFO] Clicked on {image_path}")
        time.sleep(pause)
        return True
    else:
        print(f"[WARNING] {image_path} not found on screen.")
        return False

def open_vscode():
    """
    Open Visual Studio Code via Windows Search.
    Steps:
    1) Click the Windows search button (search_button.png).
    2) Type 'visual studio code' and press Enter.
    3) Wait for VS Code to launch.
    4) Maximize the VS Code window using Win + Up.
    Returns True if VS Code is opened successfully, otherwise False.
    """
    print("[INFO] Step 1: Click the Windows search button.")
    if not locate_and_click("search_button.png", confidence=0.8, pause=1.0):
        print("[ERROR] Could not find 'search_button.png'. Aborting VS Code launch.")
        return False

    print("[INFO] Step 2: Type 'visual studio code' and press Enter.")
    pyautogui.typewrite("visual studio code", interval=0.05)
    pyautogui.press("enter")
    print("[INFO] Waiting for VS Code to open...")
    time.sleep(5)  # Adjust based on your system's performance

    print("[INFO] Step 3: Maximize VS Code window using Win + Up.")
    pyautogui.hotkey("win", "up")
    time.sleep(1)

    print("[INFO] VS Code launched and maximized successfully.")
    return True

def create_file(file_type, file_name):
    """
    Create a new file in Visual Studio Code.
    Steps:
    1) Press Ctrl + Alt + Win + N to create a new file.
    2) Select the save button based on 'file_type'.
    3) Save the file with Ctrl + Shift + S, type the file name, and press Enter.
    Returns True if the file is created and saved successfully, otherwise False.
    """
    print("[INFO] Step 1: Press Ctrl + Alt + Win + N to create a new file.")
    pyautogui.hotkey("ctrl", "alt", "win", "n")
    time.sleep(1)

    if file_type.lower() == "python":
        print("[INFO] Selecting the Python save button.")
        if not locate_and_click("python_save_button.png", confidence=0.5, pause=1.0):
            print("[ERROR] Could not find 'python_save_button.png'. Aborting file creation.")
            return False
    elif file_type.lower() == "jupyter notebook":
        print("[INFO] Selecting the Jupyter Notebook save button.")
        if not locate_and_click("jupyternotebook_save_button.png", confidence=0.5, pause=1.0):
            print("[ERROR] Could not find 'jupyternotebook_save_button.png'. Aborting file creation.")
            return False
    else:
        print(f"[ERROR] Unsupported file type: {file_type}. Aborting file creation.")
        return False

    print("[INFO] Step 2: Press Ctrl + Shift + S to save the file.")
    pyautogui.hotkey("ctrl", "shift", "s")
    time.sleep(1)

    print(f"[INFO] Step 3: Type the file name '{file_name}' and press Enter.")
    pyautogui.typewrite(file_name, interval=0.05)
    pyautogui.press("enter")
    time.sleep(1)

    print(f"[INFO] Successfully created and saved the {file_type} file as '{file_name}'.")
    return True


def save_file():
    """
    Save the current file in Visual Studio Code.
    Presses Ctrl + S to save.
    """
    print("[INFO] Saving the file using Ctrl + S.")
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)  # Allow time for the save operation
    print("[INFO] File saved successfully.")

def run_file():
    """
    Run the current file in Visual Studio Code using the Command Palette.
    Steps:
    1) Press Ctrl + Shift + P to open the Command Palette.
    2) Type 'run' (or a specific run command) and press Enter.
    Returns True if run command is executed, otherwise False.
    """
    if locate_and_click("run_button.png", confidence=0.5, pause=1.0):
        print(f"running")
    else:
        print("[WARNING] NOT Running")
    time.sleep(1)

def main():
    """
    Automate the process of opening VS Code, creating a new file,
    saving it, and running it.
    """
    input("[PROMPT] Ensure 'search_button.png' and 'createfile_button.png' are on your screen. Press Enter to continue...")

    # Step 1: Open Visual Studio Code
    if not open_vscode():
        print("[ERROR] Failed to open Visual Studio Code. Exiting.")
        sys.exit(1)

    # Step 2: Create a new Python file named 'example_script.py'
    file_type = "python"
    file_name = "example_script.py"
    if not create_file(file_type, file_name):
        print("[ERROR] Failed to create the file. Exiting.")
        sys.exit(1)

    # Step 3: Save the file
    save_file()

    # Step 4: Run the file
    if run_file():
        print("[INFO] File run command executed successfully.")
    else:
        print("[WARNING] Failed to execute the run command.")

    print("[INFO] Automation script completed. Check Visual Studio Code for results.")

if __name__ == "__main__":
    # Verify that required image files exist
    required_images = ["search_button.png", "createfile_button.png"]
    missing_images = [img for img in required_images if not os.path.isfile(img)]
    if missing_images:
        print(f"[ERROR] Missing required image(s): {', '.join(missing_images)}. Please ensure they are in the script directory.")
        sys.exit(1)

    main()
