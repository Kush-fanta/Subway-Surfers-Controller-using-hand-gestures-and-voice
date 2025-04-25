
# Subway Surfers Game Control System

Control an HTML5 (“Poki”) or emulator-based Subway Surfers with your **hand gestures** and **voice commands**, fully offline.

## Features
- **Gestures** via webcam (MediaPipe):  
  • Swipe left/right → move  
  • Up/down → jump/roll  
- **Voice** via microphone (Vosk):  
  • “left”, “right”, “jump”, “roll”, “hoverboard”  
  • Offline, low-latency keyword spotting  
- **Modes**: Audio-only, Gesture-only, Both  
- **Auto-focus** on the game window before sending keypresses

## Prerequisites
- Python 3.7–3.11  
- Windows, macOS or Linux  
- A webcam and microphone  

## Installation
1. Clone the repo:  
   ```bash
   git clone https://github.com/Kush-fanta/Subway-Surfers-Controller-using-hand-gestures-and-voice.git
   cd Subway-Surfers-Controller-using-hand-gestures-and-voice
   ```
2. (Optional) Create a venv and activate it.  
3. Install Python dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
4. Download and unpack the Vosk model into `models/vosk-model-small-en-us-0.15/`.

## Configuration
Edit `config.py` to adjust:
- `KEY_MAP` (which key each command sends)  
- `SWIPE_THRESHOLD`, `VERTICAL_THRESHOLD`, `GESTURE_COOLDOWN`  
- `EMULATOR_WINDOW_TITLE` (part of your browser/emulator window’s title)

## Usage
```bash
python main.py
```
Choose:
1. Audio-only  
2. Gesture-only  
3. Both  
4. Quit  

Say “exit” in audio mode or press ESC in gesture mode to return to the menu.


