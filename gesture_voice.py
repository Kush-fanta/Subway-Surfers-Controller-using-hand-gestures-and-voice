import os
import cv2
import mediapipe as mp
import time
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from threading import Event
from config import (
    VALID_VOICE_COMMANDS,
    SWIPE_THRESHOLD,
    VERTICAL_THRESHOLD,
    GESTURE_COOLDOWN
)
from input_controller import send_keypress

# ── MediaPipe Hands Setup ─────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# ── Gesture Detection State ───────────────────────────────────────────────────
_prev_center = None
_last_time = 0

# ── Synonym Mappings ─────────────────────────────────────────────────────────
RIGHT_SYNS = ["right", "write", "rite", "correct", "right side", "light", "turn right"]
ROLL_SYNS  = ["roll", "role", "down", "downward", "downwards"]

# ── Vosk Model Loading ────────────────────────────────────────────────────────
# The model directory must be at ./models/vosk-model-small-en-us-0.15
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models", "vosk-model-small-en-us-0.15")
if not os.path.isdir(MODEL_DIR):
    raise FileNotFoundError(
        f"Could not find Vosk model at:\n  {MODEL_DIR}\n"
        "Download and unzip the 'vosk-model-small-en-us-0.15' into the models/ folder."
    )

vosk_model = Model(MODEL_DIR)
vosk_rec   = KaldiRecognizer(
    vosk_model,
    16000,
    '["left","right","jump","roll","hoverboard","exit"]'
)
audio_q = queue.Queue()

def _vosk_callback(indata, frames, time_info, status):
    """Callback for sounddevice stream: collect raw audio frames."""
    if status:
        print(f"⚠️ Audio status: {status}")
    audio_q.put(bytes(indata))


def get_gesture(frame):
    """
    Detects hand swipe/jump/roll with MediaPipe.
    Returns one of: 'left','right','jump','roll', or None.
    """
    global _prev_center, _last_time

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)
    now = time.time()

    if res.multi_hand_landmarks:
        lm = res.multi_hand_landmarks[0]
        mp.solutions.drawing_utils.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
        xs = [p.x for p in lm.landmark]
        ys = [p.y for p in lm.landmark]
        cx = int(sum(xs) / len(xs) * w)
        cy = int(sum(ys) / len(ys) * h)

        if _prev_center and (now - _last_time) > GESTURE_COOLDOWN:
            dx, dy = cx - _prev_center[0], cy - _prev_center[1]
            # Horizontal swipe
            if abs(dx) > SWIPE_THRESHOLD and abs(dx) > abs(dy):
                _last_time = now
                return "right" if dx > 0 else "left"
            # Vertical swipe
            if abs(dy) > VERTICAL_THRESHOLD:
                _last_time = now
                return "roll" if dy > 0 else "jump"

        _prev_center = (cx, cy)

    return None


def continuous_voice_loop(stop_event: Event):
    """
    Offline Vosk voice control:
    - Streams mic audio at 16 kHz
    - Recognizes only the small set of commands
    - Fires send_keypress(...) immediately
    - Stops when 'exit' is heard or stop_event is set
    """
    print("🎧 Voice control active (offline). Say 'exit' to stop.")
    try:
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype='int16',
            channels=1,
            callback=_vosk_callback
        ):
            while not stop_event.is_set():
                data = audio_q.get()
                if vosk_rec.AcceptWaveform(data):
                    # Result is like '{"text": "left"}'
                    res = vosk_rec.Result()
                    text = eval(res).get("text", "").lower()
                    if text:
                        print(f"🔊 Heard: {text}")
                        if text == "exit":
                            print("🛑 Exit detected. Stopping voice mode.")
                            stop_event.set()
                            break

                        # Map roll first
                        for syn in ROLL_SYNS:
                            if syn in text:
                                send_keypress("roll")
                                break
                        else:
                            # Then right
                            for syn in RIGHT_SYNS:
                                if syn in text:
                                    send_keypress("right")
                                    break
                            else:
                                # Finally any other valid command
                                for cmd in VALID_VOICE_COMMANDS:
                                    if cmd in text:
                                        send_keypress(cmd)
                                        break
    except Exception as e:
        print(f"⚠️ Vosk listener error: {e}")
