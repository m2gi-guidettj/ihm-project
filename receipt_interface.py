from tkinter import Tk, Label, Canvas, PhotoImage
import PIL.Image, PIL.ImageTk
import numpy as np

class ReceiptInterface:
    def __init__(self):
        self.root = Tk()
        self.root.title("Receipt Display")
        self.receipt_label = Label(self.root, text="Current Receipt: None", font=('Helvetica', 16))
        self.receipt_label.pack(pady=20)
        self.canvas = Canvas(self.root, width=640, height=480)
        self.canvas.pack()
        self.photo = None  # To hold the photoimage reference

    def update_image(self, cv_image):
        image = PIL.Image.fromarray(cv_image)
        self.photo = PIL.ImageTk.PhotoImage(image=image)
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

    def change_receipt(self, direction):
        # Placeholder function to simulate receipt change
        if direction == "next":
            print("Changing to next receipt...")
        elif direction == "prev":
            print("Changing to previous receipt...")

    def run(self):
        self.root.mainloop()

    def close(self):
        self.root.destroy()
