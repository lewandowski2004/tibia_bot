import cv2 as cv

import pyautogui
import time
import random

from functionality_game.interactive_actions import focus_and_press_key_if_active
from utils.utilities import get_monster_count, find_next_move_point, find_previous_move_point, is_hungry


def hp_status_monitoring(hp_area_coordinates, control_flags, frame_queue, hp_point_limit, character_name, pytesseract):
    wspolrzedne_hp = hp_area_coordinates.get()
    # Usunięcie nawiasów i podzielenie ciągu na listę liczb w formie tekstowej
    coords_list = wspolrzedne_hp.strip("()").split(", ")
    # Przekształcenie listy tekstowej na krotkę zawierającą liczby całkowite
    coords_tuple = tuple(map(int, coords_list))
    while control_flags['running_HP_monitoring']:
        if frame_queue.empty():
            print("Kolejkda ramek jest pusta.")
            return
        frame = frame_queue.get_nowait()
        roi = cv.cvtColor(frame[coords_tuple[1]:coords_tuple[3], coords_tuple[0]:coords_tuple[2]],
                          cv.COLOR_BGR2GRAY)
        hp_value = pytesseract.image_to_string(roi, config='--psm 11 --oem 3 -c tessedit_char_whitelist=0123456789')
        if hp_value:
            print(f"Znaleziona liczba punktów HP1: {hp_value}")
            if int(hp_value) <= int(hp_point_limit.get()):
                print("ULECZ")
                focus_and_press_key_if_active(character_name, "1")


def mana_status_monitoring(mana_area_coordinates, control_flags, frame_queue, mana_point_limit, character_name,
                           pytesseract):
    wspolrzedne_mana = mana_area_coordinates.get()
    # Usunięcie nawiasów i podzielenie ciągu na listę liczb w formie tekstowej
    coords_list = wspolrzedne_mana.strip("()").split(", ")
    # Przekształcenie listy tekstowej na krotkę zawierającą liczby całkowite
    coords_tuple = tuple(map(int, coords_list))
    while control_flags['running_MANA_monitoring']:
        if frame_queue.empty():
            print("Kolejka ramek jest pusta.")
            return
        frame = frame_queue.get_nowait()
        roi = cv.cvtColor(frame[coords_tuple[1]:coords_tuple[3], coords_tuple[0]:coords_tuple[2]],
                          cv.COLOR_BGR2GRAY)
        mana_value = pytesseract.image_to_string(roi, config='--psm 11 --oem 3 -c tessedit_char_whitelist=0123456789')
        if mana_value:
            print(f"Znaleziona liczba punktów MANA: {mana_value}")
            if int(mana_value) <= int(mana_point_limit.get()):
                print("DODAJ MANE")
                focus_and_press_key_if_active(character_name, "2")


def move(mini_map_area_coordinates, control_flags, hunting_steps, is_auto_loot_value, frame_queue):
    mini_map = mini_map_area_coordinates.get()  # Pobierz ciąg tekstowy zawierający współrzędne
    coords_list = mini_map.strip("()").split(", ")  # Przekształcenie listy tekstowej na krotkę
    mini_map_area = tuple(map(int, coords_list))
    print("------START MOVEMENT------\n")
    while control_flags['running_hunting']:
        for key, value in hunting_steps.items():
            if value[1] == 'MOVE':
                go_to_move_point(mini_map_area, key, value[0],
                                 f'image/icon_points/icon_point_{value[0]}.PNG', control_flags, hunting_steps,
                                 is_auto_loot_value, frame_queue)


def go_to_move_point(mini_map_area_coordinates, point_index, point_number, image_path,
                     control_flags, hunting_steps, is_auto_loot_value, frame_queue):
    val_threshold = True
    counter = 0
    while val_threshold and control_flags['running_hunting'] and counter < 4:
        print(f"MOVE to point: {point_number}")
        counter += 1
        template = cv.imread(image_path, 0)
        w, h = template.shape[::-1]  # Szerokość i wysokość wzorca
        if frame_queue.empty():
            print("Kolejka ramek jest pusta.")
            return
        frame = frame_queue.get()

        roi_gray = cv.cvtColor(frame[mini_map_area_coordinates[1]:mini_map_area_coordinates[3],
                               mini_map_area_coordinates[0]:mini_map_area_coordinates[2]],
                               cv.COLOR_BGR2GRAY)

        res = cv.matchTemplate(roi_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.6

        # Znajdź lokalizację najlepszego dopasowania
        _, max_val, _, max_loc = cv.minMaxLoc(res)
        if max_val < threshold and counter == 3 and point_number == 1:
            control_flags['index_move_point'] = point_number
            next_point = find_next_move_point(hunting_steps, 1)
            print(f"Następny punkt: {next_point}")
            go_to_move_point(mini_map_area_coordinates, point_index, next_point,
                             f'image/icon_points/icon_point_{next_point}.PNG',
                             control_flags, hunting_steps, is_auto_loot_value, frame_queue)
            break
        if max_val < threshold and counter == 3 and point_number != 1:
            control_flags['index_move_point'] = point_number
            result = find_previous_move_point(hunting_steps, point_index)
            before_point, index = result
            print(f"Poprzedni punkt: {before_point}")
            go_to_move_point(mini_map_area_coordinates, point_index, before_point,
                             f'image/icon_points/icon_point_{before_point}.PNG',
                             control_flags, hunting_steps, is_auto_loot_value, frame_queue)
            next_point = find_next_move_point(hunting_steps, index)
            print(f"Następny punkt: {next_point}")
            go_to_move_point(mini_map_area_coordinates, point_index, next_point,
                             f'image/icon_points/icon_point_{next_point}.PNG',
                             control_flags, hunting_steps, is_auto_loot_value, frame_queue)
        if max_val >= threshold:
            # Środek najlepszego dopasowania
            center_x = max_loc[0] + mini_map_area_coordinates[0] + w // 2
            center_y = max_loc[1] + mini_map_area_coordinates[1] + h // 2

            print(f"Kliknięcie w środek dopasowania przy: x={center_x}, y={center_y}")

            # Kliknij PPM w środek znalezionego dopasowania
            pyautogui.click(x=center_x, y=center_y + 25, button='left')
            # Ustawienie losowych wartości dla współrzędnych x i y
            x = random.randint(100, 1000)  # Losowa wartość x między 100 a 1000
            y = random.randint(100, 700)  # Losowa wartość y między 100 a 700

            # Przesunięcie kursora do wygenerowanej losowo pozycji
            pyautogui.moveTo(x, y)
            control_flags['index_move_point'] = point_number
            val_threshold = False
            time.sleep(5)
            while get_monster_count(frame_queue) > 0:
                time.sleep(1)
            auto_loot(is_auto_loot_value)
        time.sleep(2)


def go_to_move_point_without_cd(mini_map_area, point_number, image_path, control_flags, frame_queue):
    val_threshold = True
    counter = 0
    while val_threshold and control_flags['running_hunting'] and counter < 4:
        print(f"MOVE to point CD: {point_number}")
        counter += 1
        template = cv.imread(image_path, 0)
        w, h = template.shape[::-1]  # Szerokość i wysokość wzorca
        if frame_queue.empty():
            print("Kolejka ramek jest pusta.")
            return
        frame = frame_queue.get()

        roi_gray = cv.cvtColor(frame[mini_map_area[1]:mini_map_area[3], mini_map_area[0]:mini_map_area[2]],
                               cv.COLOR_BGR2GRAY)
        res = cv.matchTemplate(roi_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.6

        # Znajdź lokalizację najlepszego dopasowania
        _, max_val, _, max_loc = cv.minMaxLoc(res)
        if max_val >= threshold:
            # Środek najlepszego dopasowania
            center_x = max_loc[0] + mini_map_area[0] + w // 2
            center_y = max_loc[1] + mini_map_area[1] + h // 2

            print(f"Kliknięcie w środek dopasowania przy: x={center_x}, y={center_y}")

            # Kliknij PPM w środek znalezionego dopasowania
            pyautogui.click(x=center_x, y=center_y + 25, button='left')
            # Ustawienie losowych wartości dla współrzędnych x i y
            x = random.randint(100, 1000)  # Losowa wartość x między 100 a 1000
            y = random.randint(100, 700)  # Losowa wartość y między 100 a 700
            time.sleep(2)
            # Przesunięcie kursora do wygenerowanej losowo pozycji
            pyautogui.moveTo(x, y)
            control_flags['index_move_point'] = point_number
            val_threshold = False
        time.sleep(1)


def attack(mini_map_area_coordinates, control_flags, number_of_monsters, character_name, frame_queue):
    mini_map = mini_map_area_coordinates.get()  # Pobierz ciąg tekstowy zawierający współrzędne
    coords_list = mini_map.strip("()").split(", ")  # Przekształcenie listy tekstowej na krotkę
    mini_map_area = tuple(map(int, coords_list))
    print("------START FIGHT------\n")
    while control_flags['running_hunting']:
        if get_monster_count(frame_queue) >= number_of_monsters.get():
            print("Attack")
            focus_and_press_key_if_active(character_name, "space")
            print(control_flags['index_move_point'])
            if control_flags['index_move_point'] != 0:
                go_to_move_point_without_cd(mini_map_area, control_flags['index_move_point'],
                                            f'image/icon_points/icon_point_{control_flags["index_move_point"]}.PNG',
                                            control_flags, frame_queue)
        time.sleep(3)


def eat(is_hungry_value, control_flags, character_name, frame_queue):
    print("------START EAT------")
    while is_hungry_value.get() and control_flags['running_hunting']:
        if is_hungry(frame_queue):
            print("EAT")
            focus_and_press_key_if_active(character_name, "3")
        time.sleep(30)


def auto_loot(is_auto_loot_value):
    if is_auto_loot_value.get():
        print("TAKE LOOT")
        pyautogui.click(798, 365, button='right')
        pyautogui.click(870, 365, button='right')
        pyautogui.click(940, 365, button='right')
        pyautogui.click(940, 435, button='right')
        pyautogui.click(940, 501, button='right')
        pyautogui.click(870, 501, button='right')
        pyautogui.click(798, 501, button='right')
        pyautogui.click(798, 435, button='right')
