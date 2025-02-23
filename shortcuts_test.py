import pyautogui

def bookmark(name):
    # Open the bookmark dialog
    pyautogui.hotkey('ctrl', 'd')
    pyautogui.sleep(0.5)  # Give time for the dialog to open

    # Type the bookmark name
    pyautogui.write(name, interval=0.1)

    # Save the bookmark
    pyautogui.press('enter')

def refresh():
    pyautogui.hotkey('ctrl', 'r')

def back():
    pyautogui.hotkey('alt', 'left')

def forward():
    pyautogui.hotkey('alt', 'right')

def snap_left():
    pyautogui.hotkey('win', 'left')

def snap_right():
    pyautogui.hotkey('win', 'right')

def switch_window():
    pyautogui.hotkey('alt', 'tab')

def maximize():
    pyautogui.hotkey('win', 'up')

def minimize():
    pyautogui.hotkey('win', 'm')

def close_window():
    pyautogui.hotkey('ctrl', 'shift', 'w')

def undo():
    pyautogui.hotkey('ctrl', 'z')

def redo():
    pyautogui.hotkey('ctrl', 'y')

def cut():
    pyautogui.hotkey('ctrl', 'x')

def copy():
    pyautogui.hotkey('ctrl', 'c')

def paste():
    pyautogui.hotkey('ctrl', 'v')
