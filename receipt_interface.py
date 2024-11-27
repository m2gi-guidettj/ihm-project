from tkinter import *

class ReceiptInterface:
    def __init__(self):
        self.root = Tk()
        self.root.title("Plaque de Cuisson Connectée")
        self.root.geometry("800x700")

        # Ajouter une étiquette principale
        label_title = Label(self.root, text="Contrôle de la Plaque de Cuisson", font=("Arial", 30, "bold"))
        label_title.pack(pady=20)

        # Créer une frame pour les contrôles
        self.frame_controls = Frame(self.root)
        self.frame_controls.pack(pady=10)

        # Ajouter un label pour afficher l'état de la plaque
        self.status_label = Label(self.root, text="Plaque de cuisson éteinte", font=("Arial", 18), fg="red")
        self.status_label.pack(pady=10)
        
        self.volume_slider = None

        # Suivi de l'état de la plaque
        self.power_state = False

        # Liste des recettes
        self.recipes = [
            {"title": "Gâteau au Chocolat", "description": "Un gâteau moelleux au chocolat, parfait pour les amateurs de sucré."},
            {"title": "Gâteau aux Pommes", "description": "Un gâteau léger avec des morceaux de pommes, idéal pour accompagner un café."},
            {"title": "Gâteau au Fromage", "description": "Un gâteau crémeux à base de fromage blanc, idéal après un repas copieux."},
            {"title": "Gâteau à la Vanille", "description": "Un classique intemporel ! Ce gâteau moelleux à la vanille est léger et parfumé."},
            {"title": "Gâteau au Citron", "description": "Un gâteau frais et acidulé avec une touche de citron. Parfait pour ceux qui aiment les saveurs acidulées."}
        ]

        # Frame pour les recettes
        self.frame_recipes = Frame(self.root)
        self.frame_recipes.pack(fill=BOTH, expand=True)

        # Ajouter les recettes
        self.create_recipes()

        # Afficher les contrôles
        self.update_controls()

    def create_recipes(self):
        """Créer les boutons pour afficher les recettes."""
        for recipe in self.recipes:
            button = Button(self.frame_recipes, text=recipe["title"], font=("Arial", 18), width=20, height=1,
                            command=lambda r=recipe: self.show_recipe_description(r))
            button.pack(pady=5)

        # Zone pour afficher la description
        self.recipe_title = Label(self.frame_recipes, text="", font=("Arial", 16, "bold"), wraplength=750, justify="center")
        self.recipe_title.pack(pady=10)

        self.recipe_description = Label(self.frame_recipes, text="", font=("Arial", 13), wraplength=750, justify="left")
        self.recipe_description.pack(pady=10)

    def show_recipe_description(self, recipe):
        """Afficher la description de la recette sélectionnée."""
        self.recipe_title.config(text=recipe["title"])
        self.recipe_description.config(text=recipe["description"])

    def update_controls(self):
        """Met à jour les contrôles en fonction de l'état de la plaque."""
        # Efface les anciens widgets dans la frame des contrôles
        for widget in self.frame_controls.winfo_children():
            widget.destroy()

        # Afficher le bouton en fonction de l'état
        if not self.power_state:
            power_button = Button(
                self.frame_controls,
                text="Allumer",
                font=("Arial", 20, "bold"),
                width=15,
                height=2,
                command=self.toggle_power
            )
            power_button.pack(pady=20)
        else:
            off_button = Button(
                self.frame_controls,
                text="Éteindre",
                font=("Arial", 20, "bold"),
                width=15,
                height=2,
                command=self.toggle_power
            )
            off_button.pack(pady=20)

    def toggle_power(self):
        """Alterner entre Allumer et Éteindre la plaque de cuisson."""
        self.power_state = not self.power_state
        if self.power_state:
            self.status_label.config(text="Plaque de cuisson allumée", fg="green")
        else:
            self.status_label.config(text="Plaque de cuisson éteinte", fg="red")

        # Mettre à jour les contrôles après changement d'état
        self.update_controls()

    def run(self):
        """Lancer l'interface graphique."""
        self.root.mainloop()


if __name__ == "__main__":
    interface = ReceiptInterface()
    interface.run()
