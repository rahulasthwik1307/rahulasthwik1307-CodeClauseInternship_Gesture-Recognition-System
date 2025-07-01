import cv2
import mediapipe as mp
import time
import numpy as np
from directkeys import right_pressed, left_pressed, PressKey, ReleaseKey, KeyIsPressed

# Configuration
KEY_PRESS_DELAY = 0.05
GESTURE_HOLD_TIME = 0.3

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

# Video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Gesture tracking
last_gesture_time = time.time()
prev_frame_time = time.time()
last_key_state = {"left": False, "right": False}
current_gesture = "NEUTRAL"

def is_fist(landmarks):
    folded = 0
    tips = [4, 8, 12, 16, 20]
    if landmarks[tips[0]].x > landmarks[tips[0]-1].x:
        folded += 1
    for i in range(1, 5):
        if landmarks[tips[i]].y > landmarks[tips[i]-2].y:
            folded += 1
    return folded >= 4

def is_open_hand(landmarks):
    extended = 0
    tips = [8, 12, 16, 20]
    for i in tips:
        if landmarks[i].y < landmarks[i-2].y:
            extended += 1
    return extended >= 3

def update_key_state(key, should_press):
    if should_press and not last_key_state[key]:
        PressKey(left_pressed if key == "left" else right_pressed)
        last_key_state[key] = True
    elif not should_press and last_key_state[key]:
        ReleaseKey(left_pressed if key == "left" else right_pressed)
        last_key_state[key] = False

# Instructions in terminal (you can remove emojis here too if needed)
print("""
[Gesture Control - Hill Climb Racing]
✊ Fist       = Brake (Left Arrow)
🖐 Open Hand = Gas (Right Arrow)
🤚 Neutral   = No Input
Press 'q' to quit.
""")

cv2.namedWindow("Gesture Control", cv2.WINDOW_NORMAL)
cv2.moveWindow("Gesture Control", 100, 50)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    gesture = "NEUTRAL"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            if is_fist(lm):
                gesture = "BRAKE"
            elif is_open_hand(lm):
                gesture = "GAS"

            # Enhanced drawing
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2)
            )

    # Banner overlay based on gesture
    banner_color = (0, 0, 255) if gesture == "BRAKE" else (0, 255, 0) if gesture == "GAS" else (100, 100, 100)
    cv2.rectangle(frame, (0, 0), (640, 40), banner_color, -1)
    cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Update keys
    if gesture == "BRAKE":
        update_key_state("left", True)
        update_key_state("right", False)
    elif gesture == "GAS":
        update_key_state("right", True)
        update_key_state("left", False)
    else:
        update_key_state("left", False)
        update_key_state("right", False)

    # FPS Counter
    curr_time = time.time()
    fps = int(1 / (curr_time - prev_frame_time + 1e-5))
    prev_frame_time = curr_time
    cv2.putText(frame, f"FPS: {fps}", (520, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # Key state info
    cv2.putText(frame, f"Keys: L={last_key_state['left']} R={last_key_state['right']}",
                (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Instruction panel (emoji-free for compatibility)
    cv2.rectangle(frame, (0, 440), (640, 480), (50, 50, 50), -1)
    cv2.putText(frame, "Fist = Brake | Open Hand = Gas | Press 'q' to quit", (10, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Gesture Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
for key in last_key_state:
    if last_key_state[key]:
        ReleaseKey(left_pressed if key == "left" else right_pressed)
cap.release()
cv2.destroyAllWindows()
