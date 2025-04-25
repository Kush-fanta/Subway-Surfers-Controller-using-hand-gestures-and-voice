import cv2
import threading
from gesture_voice import get_gesture, continuous_voice_loop  # updated
from input_controller import send_keypress
from feedback_utils import draw_feedback
from threading import Event

def gesture_loop(stop_event: Event):
    """
    Activates webcam to detect gestures and trigger game commands.
    Press ESC to exit gesture mode.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Webcam not available.")
        return

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Mirror correction
        cmd = get_gesture(frame)
        if cmd:
            send_keypress(cmd)

        draw_feedback(frame, cmd)
        cv2.imshow("Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            stop_event.set()
            break

    cap.release()
    cv2.destroyAllWindows()


def voice_loop(stop_event: Event):
    """
    Starts continuous voice command recognition.
    """
    try:
        continuous_voice_loop(stop_event)
    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt—returning to menu.")
        stop_event.set()


def main():
    """
    Main menu loop for selecting control mode.
    """
    while True:
        print("""
Select control mode:
  1) Audio only   (say "exit" or press Ctrl+C to return)
  2) Gesture only (press ESC in the video window to return)
  3) Both         (either ESC or "exit"/Ctrl+C will return)
  4) Quit program
""")
        choice = input("Enter 1, 2, 3 or 4: ").strip()
        stop_event = Event()

        if choice == "1":
            print("🎤 AUDIO‑ONLY mode. Listening for commands…")
            voice_loop(stop_event)

        elif choice == "2":
            print("🖐️ GESTURE‑ONLY mode. Use your hand; ESC to exit…")
            gesture_loop(stop_event)

        elif choice == "3":
            print("🔀 BOTH modes active. ESC or 'exit'/Ctrl+C will stop…")
            t1 = threading.Thread(target=gesture_loop, args=(stop_event,), daemon=True)
            t2 = threading.Thread(target=voice_loop, args=(stop_event,), daemon=True)
            t1.start()
            t2.start()
            t1.join()
            stop_event.set()
            t2.join()

        elif choice == "4":
            print("👋 Exiting program. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")
            continue

        print("\n🔄 Returning to mode selection…\n")


if __name__ == "__main__":
    main()
