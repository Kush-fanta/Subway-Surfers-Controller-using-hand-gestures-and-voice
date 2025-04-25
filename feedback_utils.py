# feedback_utils.py

import cv2

# Text style
font       = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
color      = (0, 255, 0)  # Green
thickness  = 2
position   = (50, 50)

def draw_feedback(frame, command):
    """
    Draws the detected gesture or voice command on the frame.
    """
    if command:
        text = f"Command: {command.upper()}"
        cv2.putText(frame, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
