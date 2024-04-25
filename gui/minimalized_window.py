import cv2 as cv

import tkinter as tk
from tkinter import Label
from tkinter import font as tkFont
import queue
from PIL import Image, ImageTk


def open_minimized_window(master, frame_queue):
    # Ukrywanie głównego okna
    master.withdraw()
    # Tworzenie nowego, mniejszego okna
    minimized_window = tk.Toplevel()

    window_width = 204
    window_height = 42
    screen_height = minimized_window.winfo_screenheight()
    x_position = 0
    y_position = screen_height - window_height - 40

    # Ustawienie rozmiaru i pozycji okna
    minimized_window.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

    minimized_window.overrideredirect(True)  # Usuwa ramki okna
    minimized_window.wm_attributes("-topmost", 1)  # Okno zawsze na wierzchu
    minimized_window.configure(bg='yellow')

    # Tworzenie Label, który będzie wyświetlał obraz
    image_label = Label(minimized_window)
    image_label.pack(side=tk.LEFT, padx=(3, 0))

    # Stylowanie przycisku
    custom_font = tkFont.Font(size=14, weight="bold")
    restore_button = tk.Button(minimized_window, text=">",
                               command=lambda: restore_main_window(master, minimized_window),
                               font=custom_font, height=0, width=2, padx=0, pady=0)
    restore_button.pack(side=tk.LEFT)

    update_image(frame_queue, minimized_window, image_label)


def update_image(frame_queue, minimized_window, image_label):
    try:
        frame = frame_queue.get_nowait()
    except queue.Empty:
        minimized_window.after(100,
                               update_image(frame_queue, minimized_window, image_label))
        return
    coords_tuple = (1745, 276, 1907, 308)

    roi = frame[coords_tuple[1]:coords_tuple[3], coords_tuple[0]:coords_tuple[2]]
    img = Image.fromarray(cv.cvtColor(roi, cv.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    image_label.imgtk = imgtk
    image_label.config(image=imgtk)
    minimized_window.after(100,
                           update_image(frame_queue, minimized_window, image_label))


def restore_main_window(master, minimized_window):
    minimized_window.destroy()
    master.deiconify()
