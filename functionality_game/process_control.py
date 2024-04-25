import threading

from pynput.mouse import Listener
from config import CAMERA_INDEX
from functionality_game.game_actions import hp_status_monitoring, mana_status_monitoring, move, attack, eat


def start_healing(cap, hp_area_coordinates, mana_area_coordinates, control_flags, frame_queue,
                  hp_point_limit, mana_point_limit, character_name, pytesseract):
    if not cap.isOpened():
        print(f"Nie można otworzyć kamery o indeksie {CAMERA_INDEX}")
        exit()

    if not control_flags['running_HP_monitoring']:
        control_flags['running_HP_monitoring'] = True
        threading.Thread(
            target=hp_status_monitoring,
            args=(
                hp_area_coordinates,
                control_flags,
                frame_queue,
                hp_point_limit,
                character_name,
                pytesseract
            )
        ).start()
    if not control_flags['running_MANA_monitoring']:
        control_flags['running_MANA_monitoring'] = True
        threading.Thread(
            target=mana_status_monitoring,
            args=(
                mana_area_coordinates,
                control_flags,
                frame_queue,
                mana_point_limit,
                character_name,
                pytesseract
            )
        ).start()


def stop_healing(control_flags):
    control_flags['running_HP_monitoring'] = False
    control_flags['running_MANA_monitoring'] = False


def start_hunting(cap, mini_map_area_coordinates, control_flags, hunting_steps,
                  number_of_monsters, character_name, is_auto_loot_value, frame_queue, is_hungry_value):
    if not cap.isOpened():
        print(f"Nie można otworzyć kamery o indeksie {CAMERA_INDEX}")
        exit()
    if not control_flags['running_hunting']:
        control_flags['running_hunting'] = True
        threading.Thread(
            target=move,
            args=(
                mini_map_area_coordinates,
                control_flags,
                hunting_steps,
                is_auto_loot_value,
                frame_queue
            )
        ).start()
        threading.Thread(
            target=attack,
            args=(
                mini_map_area_coordinates,
                control_flags,
                number_of_monsters,
                character_name,
                frame_queue
            )
        ).start()
    if is_hungry_value.get():
        threading.Thread(
            target=eat,
            args=(
                is_hungry_value,
                control_flags,
                character_name,
                frame_queue
            )
        ).start()


def stop_hunting(control_flags):
    control_flags['running_hunting'] = False
    control_flags['index_move_point'] = 0


def start_mouse_listen(button_id, hp_area_coordinates, mana_area_coordinates, minimap_area_coordinates):
    threading.Thread(target=mouse_listen, args=(button_id, hp_area_coordinates, mana_area_coordinates,
                                                minimap_area_coordinates)).start()


def mouse_listen(button_id, hp_area_coordinates, mana_area_coordinates, minimap_area_coordinates):
    with Listener(
            on_click=lambda x, y, button, pressed: on_click(x, y, button, pressed, button_id, hp_area_coordinates,
                                                            mana_area_coordinates, minimap_area_coordinates)) as listener:
        listener.join()


start_x, start_y = None, None


def on_click(x, y, button, pressed, button_id, hp_area_coordinates, mana_area_coordinates, minimap_area_coordinates):
    global start_x, start_y
    if pressed:
        start_x, start_y = x, y
    else:
        end_x, end_y = x, y
        coordinates_str = f"({start_x}, {start_y - 30}, {end_x}, {end_y - 20})"
        if button_id == 1:
            hp_area_coordinates.set(coordinates_str)
        if button_id == 2:
            mana_area_coordinates.set(coordinates_str)
        if button_id == 3:
            minimap_area_coordinates.set(coordinates_str)
        return False  # Zatrzymuje nasłuchiwanie
