from tkinter import *
from PIL import Image, ImageTk
from PIL.Image import Resampling

class ReceiptInterface:
    def __init__(self):
        self.root = Tk()
        self.root.title("Recettes et Détails")
        self.root.geometry("800x700")

        # Liste des recettes
        self.recipes = [
            {
                "title": "Gâteau au Chocolat",
                "description": "Un gâteau moelleux au chocolat, parfait pour les amateurs de sucré.",
                "image": "chocolate_cake.jpg"
            },
            {
                "title": "Gâteau aux Pommes",
                "description": "Un gâteau léger avec des morceaux de pommes, idéal pour accompagner un café.",
                "image": "apple_cake.jpg"
            },
            {
                "title": "Gâteau au Fromage",
                "description": "Un gâteau crémeux à base de fromage blanc, idéal après un repas copieux.",
                "image": "cheese_cake.jpg"
            },
            {
                "title": "Gâteau au Citron",
                "description": "Un gâteau frais et acidulé avec une touche de citron. Parfait pour ceux qui aiment les saveurs acidulées.",
                "image": "lemon_cake.jpg"
            }
        ]

        # Ajouter une étiquette principale
        label_title = Label(self.root, text="Recettes Disponibles", font=("Arial", 24, "bold"))
        label_title.pack(pady=20)

        # Frame pour les recettes
        self.recipes_frame = Frame(self.root)
        self.recipes_frame.pack(fill=BOTH, expand=True)

        self.display_recipes()

    def display_recipes(self):
        """Afficher les recettes avec leurs images et descriptions succinctes."""
        for recipe in self.recipes:
            # Charger l'image
            try:
                img = Image.open(recipe["image"])
                img = img.resize((100, 100), Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Erreur de chargement d'image : {e}")
                photo = None

            # Cadre pour chaque recette
            recipe_frame = Frame(self.recipes_frame, bd=2, relief=SOLID, padx=10, pady=10)
            recipe_frame.pack(pady=10, fill=X)

            # Afficher l'image
            if photo:
                img_label = Label(recipe_frame, image=photo)
                img_label.image = photo
                img_label.pack(side=LEFT, padx=10)

            # Texte : titre et bouton
            text_frame = Frame(recipe_frame)
            text_frame.pack(side=LEFT, fill=BOTH, expand=True)

            title_label = Label(text_frame, text=recipe["title"], font=("Arial", 16, "bold"))
            title_label.pack(anchor=W)

            button = Button(
                text_frame,
                text="Voir Détails",
                command=lambda r=recipe: self.show_recipe_details(r),
                font=("Arial", 14, "bold"),  # Augmenter la taille du texte
                width=110,  # Taille du bouton
                height=2,  # Taille du bouton
               
            )
            button.pack(anchor=W, pady=10)

    def show_recipe_details(self, recipe):
        """Afficher une nouvelle fenêtre avec les détails de la recette."""
        details_window = Toplevel(self.root)
        details_window.title(recipe["title"])

        # Titre de la recette
        title_label = Label(details_window, text=recipe["title"], font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # Charger et afficher l'image
        try:
            img = Image.open(recipe["image"])
            img = img.resize((200, 200), Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = Label(details_window, image=photo)
            img_label.image = photo
            img_label.pack(pady=10)
        except Exception as e:
            print(f"Erreur de chargement d'image pour les détails : {e}")

        # Description
        desc_label = Label(details_window, text=recipe["description"], font=("Arial", 14), wraplength=380, justify="left")
        desc_label.pack(pady=10)

        # Bouton Quitter avec un bouton plus grand
        quit_button = Button(
            details_window,
            text="Quitter",
            font=("Arial", 16, "bold"),
            bg="red",
            fg="white",
            width=55,  # Taille du bouton
            height=4,  # Taille du bouton
            command=details_window.destroy
        )
        quit_button.pack(pady=20)

    def run(self):
        """Lancer l'interface graphique."""
        self.root.mainloop()
        
        
if __name__ == "__main__":
    interface = ReceiptInterface()
    interface.run()