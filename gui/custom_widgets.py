import tkinter as tk
from tkinter import PhotoImage, Label, IntVar
from tkinter import ttk


class MovementPointRadioButton(tk.Frame):
    def __init__(self, master, image_path, move_point_value, value, app_instance, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.value = value
        self.var = IntVar()
        self.app_instance = app_instance

        original_img = PhotoImage(file=image_path)
        # Powiększ obraz
        zoomed_img = original_img.zoom(3)
        self.img = zoomed_img.subsample(2)

        self.label = Label(self, image=self.img)
        self.label.grid(row=1, column=0)

        # Tworzenie i umieszczanie checkboxa
        self.checkbox = ttk.Radiobutton(self, variable=move_point_value, style='Custom.TRadiobutton', value=value)
        self.checkbox.grid(row=2, column=0)