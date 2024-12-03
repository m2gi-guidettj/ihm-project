import cv2
import mediapipe as mp
import pyautogui
from threading import Thread
from receipt_interface import ReceiptInterface
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer

q = queue.Queue()  # File pour l'audio
command_queue = queue.Queue()  # File pour les commandes

# Suivi de l'état de la plaque
power_state = False

def toggle_power():
    """Alterner entre Allumer et Éteindre la plaque de cuisson."""
    global power_state  # Utilisation de la variable globale
    power_state = not power_state
    if power_state:
        print("Plaque de cuisson allumée")
    else:
        print("Plaque de cuisson éteinte")


def calculate_distance(point1, point2):
    """Calcule la distance euclidienne entre deux points."""
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2) ** 0.5

def process_gestures(interface):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils
    screen_width, screen_height = pyautogui.size()
    cap = cv2.VideoCapture(0)

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
                pyautogui.moveTo(x, y)

                distance = calculate_distance(middle_tip, thumb_tip)

                if distance < 0.05:  # Ajuster le seuil si nécessaire
                    pyautogui.click()  # Effectuer un clic
                    print("Sélection effectuée !")

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def callback(indata, frames, time, status):
    """Callback pour traiter les blocs audio."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def process_voice_commands(interface):
    """Traitement des commandes vocales pour contrôler l'interface."""
    try:
        model = Model(lang="fr")  # Utiliser le modèle en français
        samplerate = 16000  # Définir une fréquence d'échantillonnage par défaut

        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype="int16", channels=1, callback=callback):
            print("Détection vocale en cours...")

            recognizer = KaldiRecognizer(model, samplerate)

            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    print(f"Reconnu : {result}")

                    # Envoi des commandes à la file pour le thread principal
                    if "allumez" in result:
                        print("Commande reçue : Allumer la plaque")
                        command_queue.put("toggle_power")
                    elif "éteindre" in result:
                        print("Commande reçue : Éteindre la plaque")
                        command_queue.put("toggle_power")
                    elif "recette" in result:
                        print("Commande reçue : Afficher les recettes")
                        command_queue.put("show_recipes")
                    elif "quitter" in result:
                        print("Commande reçue : Quitter")
                        command_queue.put("quit")
                        break

    except KeyboardInterrupt:
        print("\nDétection vocale arrêtée.")
    except Exception as e:
        print(f"Erreur : {e}", file=sys.stderr)

def process_commands(interface):
    """Traitement des commandes dans le thread principal."""
    while True:
        command = command_queue.get()
        if command == "toggle_power":
            toggle_power()  # Appeler la fonction toggle_power depuis main
        elif command == "show_recipes":
            interface.run()  # Afficher les recettes
        elif command == "quit":
            interface.root.destroy()

if __name__ == "__main__":
    interface = ReceiptInterface()

    # Thread pour la détection des gestes
    gesture_thread = Thread(target=process_gestures, args=(interface,))
    gesture_thread.start()

    # Thread pour la détection des commandes vocales
    voice_thread = Thread(target=process_voice_commands, args=(interface,))
    voice_thread.start()

    # Thread pour l'exécution de l'interface
    interface_thread = Thread(target=interface.run)
    interface_thread.start()

    # Gérer les commandes dans le thread principal
    process_commands(interface)

    # Attendre la fin des threads
    gesture_thread.join()
    voice_thread.join()
    interface_thread.join()