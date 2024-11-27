import cv2
import mediapipe as mp
import pyautogui
from threading import Thread
from receipt_interface import ReceiptInterface

def process_gestures(interface):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils
    screen_width, screen_height = pyautogui.size()
    cap = cv2.VideoCapture(0)
    prev_x, prev_y = None, None

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
                mp_drawing.draw_landmarks(rgb_frame, landmarks, mp_hands.HAND_CONNECTIONS)

                index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                if handedness == "Right":
                    x, y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)
                    if prev_x is not None and prev_y is not None:
                        dx, dy = x - prev_x, y - prev_y

                        if abs(dy) > abs(dx):
                            if dy > 50:
                                interface.change_receipt("prev")
                            elif dy < -50:
                                interface.change_receipt("next")

                    prev_x, prev_y = x, y

        interface.update_image(cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))  # Update the GUI with the frame

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    interface = ReceiptInterface()
    thread = Thread(target=process_gestures, args=(interface,))
    thread.start()
    interface.run()  # Runs in the main thread
    thread.join()
