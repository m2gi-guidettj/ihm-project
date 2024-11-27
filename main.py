import cv2
import mediapipe as mp
import pyautogui
from threading import Thread
import tkinter as tk
from receipt_interface import ReceiptInterface

class ReceiptInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Recettes de Gâteaux")
        self.root.geometry("800x600")

        # Ajouter une étiquette principale
        label_title = tk.Label(self.root, text="5 Recettes de Gâteaux", font=("Arial", 24))
        label_title.pack(pady=20)

        # Liste des recettes
        self.recipes = [
            {"title": "Gâteau au Chocolat", "description": "Un gâteau moelleux au chocolat, parfait pour les amateurs de sucré."},
            {"title": "Gâteau aux Pommes", "description": "Un gâteau léger avec des morceaux de pommes, idéal pour accompagner un café."},
            {"title": "Gâteau au Fromage", "description": "Un gâteau crémeux à base de fromage blanc, idéal après un repas copieux."},
            {"title": "Gâteau à la Vanille", "description": "Un classique intemporel ! Ce gâteau moelleux à la vanille est léger et parfumé."},
            {"title": "Gâteau au Citron", "description": "Un gâteau frais et acidulé avec une touche de citron. Parfait pour ceux qui aiment les saveurs acidulées."}
        ]

        # Créer les frames pour les boutons et descriptions
        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.pack(pady=20)
        self.frame_description = tk.Frame(self.root)
        self.frame_description.pack(fill=tk.BOTH, expand=True)

        # Créer les boutons des recettes
        for recipe in self.recipes:
            self.create_button(recipe)

    def create_button(self, recipe):
        button = tk.Button(self.frame_buttons, text=recipe["title"], font=("Arial", 14), width=20, height=2,
                           command=lambda: self.show_recipe_description(recipe))
        button.pack(pady=5)

    def show_recipe_description(self, recipe):
        for widget in self.frame_description.winfo_children():
            widget.destroy()
        recipe_title = tk.Label(self.frame_description, text=recipe["title"], font=("Arial", 20, "bold"))
        recipe_title.pack(pady=10)
        recipe_description = tk.Label(self.frame_description, text=recipe["description"], font=("Arial", 14), wraplength=750)
        recipe_description.pack(pady=10)

    def run(self):
        self.root.mainloop()


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
                middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                # Déplacer la souris avec le majeur
                x, y = int(middle_tip.x * screen_width), int(middle_tip.y * screen_height)
                pyautogui.moveTo(x, y)

                # Détecter si le majeur et le pouce se touchent
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
