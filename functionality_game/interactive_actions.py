import pygetwindow as gw
import pyautogui


def focus_and_press_key_if_active(character_name, key_to_press):
    window_title = f"Tibia - {character_name.get()}"  # Ustawienie stałego tytułu okna
    active_window = gw.getActiveWindow()  # Pobranie aktualnie aktywnego okna

    # Sprawdzenie, czy aktywne okno ma tytuł 'Tibia'
    if active_window and active_window.title == window_title:
        pyautogui.press(key_to_press)
    else:
        print(f"Okno '{window_title}' nie jest aktywne.")