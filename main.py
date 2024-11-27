import cv2
import mediapipe as mp
import pyautogui
from threading import Thread
from receipt_interface import ReceiptInterface


def calculate_distance(point1, point2):
    """Calcule la distance euclidienne entre deux points."""
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2) ** 0.5


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
                # Détecter les points du majeur et du pouce
                index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                x, y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)
                 # Envoyer les nouvelles coordonnées à la queue
                pyautogui.moveTo(x, y)
                
                distance = calculate_distance(middle_tip, thumb_tip)
                
                if distance < 0.05:  # Ajuster le seuil si nécessaire
                    pyautogui.click()  # Effectuer un clic
                    print("Sélection effectuée !")

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
