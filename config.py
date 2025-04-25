# config.py

# Key mappings (used by input_controller.py)
KEY_MAP = {
    "left": "left",         # Arrow key left
    "right": "right",       # Arrow key right
    "write": "right",       # Treat "write" as "right"
    "jump": "up",           # Arrow key up
    "roll": "down",         # Arrow key down
    "hoverboard": "space"   # Spacebar to activate hoverboard
}

# Gesture detection thresholds
SWIPE_THRESHOLD = 40        # Min pixel movement for left/right swipe
VERTICAL_THRESHOLD = 40     # Min pixel movement for jump/roll

# Gesture detection timing
GESTURE_COOLDOWN = 1.0      # Seconds between gesture triggers

# Voice recognition
VALID_VOICE_COMMANDS = ["left", "right", "write", "jump", "roll", "hoverboard", "exit"]
# Wake word (unused right now)
WAKE_WORD = None            

# Title (or unique substring) of your Poki browser window/tab
EMULATOR_WINDOW_TITLE = "SUBWAY SURFERS - Play Online for Free! | Poki - Brave"
