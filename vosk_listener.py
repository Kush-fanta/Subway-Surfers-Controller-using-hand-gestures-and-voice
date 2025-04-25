import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# 1. Load model
model = Model("models/vosk-model-small-en-us-0.15")

# 2. Build a recognizer with your small vocab
# We’ll only care about these words:
vocab = ["left","right","jump","roll","hoverboard","exit"]
rec = KaldiRecognizer(model, 16000, '["' + '","'.join(vocab) + '"]')

# 3. A thread-safe queue to collect audio data
q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(f"⚠️ Audio status: {status}")
    q.put(bytes(indata))

def main():
    print("🎧 Vosk listener started. Speak your commands…")
    # 4. Start streaming from the default mic
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                # result is a JSON string like: {"text": "left"}
                text = eval(result)["text"]
                if text:
                    print("🔊 Heard:", text)
                    if text == "exit":
                        break

if __name__ == "__main__":
    main()
