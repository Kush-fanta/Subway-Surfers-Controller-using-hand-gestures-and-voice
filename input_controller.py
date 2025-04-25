# input_controller.py

import time
import pyautogui
import pygetwindow as gw
from config import KEY_MAP, EMULATOR_WINDOW_TITLE

def focus_game_window():
    """
    Brings the game window to front if possible.
    Any errors—including WinError 0—are ignored.
    """
    wins = gw.getWindowsWithTitle(EMULATOR_WINDOW_TITLE)
    if not wins:
        print(f"⚠️  Couldn’t find window titled '{EMULATOR_WINDOW_TITLE}'")
        return
    win = wins[0]
    try:
        if win.isMinimized:
            win.restore()
        win.activate()
        time.sleep(0.1)  # small pause to let Windows catch up
    except Exception:
        # swallow *all* exceptions
        pass

def send_keypress(command: str):
    """
    Simulates a key press for the given command.
    Will attempt to focus the window but never aborts on failure.
    """
    if command not in KEY_MAP:
        print(f"⚠️  Unknown command: {command}")
        return

    # Try to focus, but don't bail out if it fails
    focus_game_window()

    key = KEY_MAP[command]
    print(f"⌨️  Sending '{key}'")
    try:
        pyautogui.press(key)
    except Exception as e:
        # Log but never abort on benign WinError 0
        print(f"⚠️  Keypress error (ignored): {e}")
