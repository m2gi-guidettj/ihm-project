import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_drawing = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)
prev_x, prev_y = None, None

def change_receipt(direction):
    # Placeholder function to simulate receipt change
    if direction == "next":
        print("Changing to next receipt...")
    elif direction == "prev":
        print("Changing to previous receipt...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            handedness = results.multi_handedness[results.multi_hand_landmarks.index(landmarks)].classification[0].label
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_pip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

            if handedness == "Right":
                x, y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)
                if prev_x is not None and prev_y is not None:
                    dx, dy = x - prev_x, y - prev_y

                    if abs(dy) > abs(dx):  # Detects a vertical swipe
                        if dy > 50:  # Swipe down
                            change_receipt("prev")
                        elif dy < -50:  # Swipe up
                            change_receipt("next")

                prev_x, prev_y = x, y

    cv2.imshow("Gesture Recognition", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
