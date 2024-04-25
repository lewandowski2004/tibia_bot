import cv2 as cv


def find_previous_move_point(hunting_steps, start_index):
    # Przeszukujemy słownik wstecz od start_index - 1 do 1 (minimalny klucz)
    for i in range(start_index - 1, 0, -1):
        if i in hunting_steps:  # Sprawdzamy, czy istnieje klucz
            return (hunting_steps[i][0], i)  # Zwracamy pierwszy element krotki oraz indeks
    return None  # Jeżeli nie znajdziemy, zwracamy None


def find_next_move_point(hunting_steps, start_index):
    # Przeszukujemy słownik do przodu od start_index + 1 do maksymalnego klucza
    max_key = max(hunting_steps.keys())  # Pobieramy maksymalny klucz z słownika
    print(f"MAX KEY: {max_key}")
    for i in range(start_index + 1, max_key + 1):
        print(f"INDEX: {i}")
        if i in hunting_steps:  # Sprawdzamy, czy istnieje klucz
            return hunting_steps[i][0]  # Zwracamy pierwszy element krotki
    return None  # Jeżeli nie znajdziemy, zwracamy None


def get_monster_count(frame_queue):
    first_slot_battle_list_area = (1572, 63, 1698, 83)
    second_slot_battle_list_area = (1572, 85, 1698, 105)
    third_slot_battle_list_area = (1572, 107, 1698, 127)
    fourth_slot_battle_list_area = (1572, 129, 1698, 149)
    frame = frame_queue.get()
    roi_first_slot_battle_list_area = frame[first_slot_battle_list_area[1]:first_slot_battle_list_area[3],
                                      first_slot_battle_list_area[0]:first_slot_battle_list_area[2]]
    roi_second_slot_battle_list_area = frame[second_slot_battle_list_area[1]:second_slot_battle_list_area[3],
                                       second_slot_battle_list_area[0]:second_slot_battle_list_area[2]]
    roi_third_slot_battle_list_area = frame[third_slot_battle_list_area[1]:third_slot_battle_list_area[3],
                                      third_slot_battle_list_area[0]:third_slot_battle_list_area[2]]
    roi_fourth_slot_battle_list_area = frame[fourth_slot_battle_list_area[1]:fourth_slot_battle_list_area[3],
                                       fourth_slot_battle_list_area[0]:fourth_slot_battle_list_area[2]]
    # cv.imwrite("test_fight.png", roi_first_slot_battle_list_area)
    # cv.imwrite("test_fight2.png", roi_second_slot_battle_list_area)
    # cv.imwrite("test_fight3.png", roi_third_slot_battle_list_area)
    # cv.imwrite("test_fight4.png", roi_fourth_slot_battle_list_area)
    reference_image_first_slot = cv.imread('image/client_setup/first_slot_battle_list.png')
    reference_image_first_slot = cv.resize(reference_image_first_slot,
                                           (first_slot_battle_list_area[2] - first_slot_battle_list_area[0],
                                            first_slot_battle_list_area[3] - first_slot_battle_list_area[1]))

    # Obliczanie różnicy
    difference_first_slot = cv.absdiff(roi_first_slot_battle_list_area, reference_image_first_slot)
    # Konwersja różnicy na obraz w skali szarości
    gray_difference_first_slot = cv.cvtColor(difference_first_slot, cv.COLOR_BGR2GRAY)
    # Progowanie, aby zaznaczyć różnice
    _, threshold_image_first_slot = cv.threshold(gray_difference_first_slot, 30, 255, cv.THRESH_BINARY)

    if get_difference_percentage(threshold_image_first_slot) > 2:
        reference_image_second_slot = cv.imread('image/client_setup/second_slot_battle_list.png')
        reference_image_second_slot = cv.resize(reference_image_second_slot,
                                                (second_slot_battle_list_area[2] - second_slot_battle_list_area[0],
                                                 second_slot_battle_list_area[3] - second_slot_battle_list_area[1]))
        difference_second_slot = cv.absdiff(roi_second_slot_battle_list_area, reference_image_second_slot)
        gray_difference_second_slot = cv.cvtColor(difference_second_slot, cv.COLOR_BGR2GRAY)
        _, threshold_image_second_slot = cv.threshold(gray_difference_second_slot, 30, 255, cv.THRESH_BINARY)

        if get_difference_percentage(threshold_image_second_slot) > 2:
            reference_image_third_slot = cv.imread('image/client_setup/third_slot_battle_list.png')
            reference_image_third_slot = cv.resize(reference_image_third_slot,
                                                   (third_slot_battle_list_area[2] - third_slot_battle_list_area[0],
                                                    third_slot_battle_list_area[3] - third_slot_battle_list_area[
                                                        1]))
            difference_third_slot = cv.absdiff(roi_third_slot_battle_list_area, reference_image_third_slot)
            gray_difference_third_slot = cv.cvtColor(difference_third_slot, cv.COLOR_BGR2GRAY)
            _, threshold_image_third_slot = cv.threshold(gray_difference_third_slot, 30, 255, cv.THRESH_BINARY)

            if get_difference_percentage(threshold_image_third_slot) > 2:
                reference_image_fourth_slot = cv.imread('image/client_setup/fourth_slot_battle_list.png')
                reference_image_fourth_slot = cv.resize(reference_image_fourth_slot,
                                                        (fourth_slot_battle_list_area[2] -
                                                         fourth_slot_battle_list_area[0],
                                                         fourth_slot_battle_list_area[3] -
                                                         fourth_slot_battle_list_area[1]))
                difference_fourth_slot = cv.absdiff(roi_fourth_slot_battle_list_area, reference_image_fourth_slot)
                gray_difference_fourth_slot = cv.cvtColor(difference_fourth_slot, cv.COLOR_BGR2GRAY)
                _, threshold_image_fourth_slot = cv.threshold(gray_difference_fourth_slot, 30, 255,
                                                              cv.THRESH_BINARY)

                if get_difference_percentage(threshold_image_fourth_slot) > 2:
                    return 4
                return 3
            return 2
        return 1
    return 0


def get_difference_percentage(threshold_image):
    non_zero_pixels = cv.countNonZero(threshold_image)
    total_pixels = threshold_image.size
    return (non_zero_pixels / total_pixels) * 100


def is_hungry(frame_queue):
    coords_tuple = (843, 3, 894, 30)
    frame = frame_queue.get()
    hunger_icon_img = cv.imread('image/icon_character_effect/hunger_icon.PNG', 0)
    roi_gray = cv.cvtColor(frame[coords_tuple[1]:coords_tuple[3], coords_tuple[0]:coords_tuple[2]],
                           cv.COLOR_BGR2GRAY)
    cv.imwrite("hungry.png", roi_gray)
    # Dopasuj wzorzec
    res = cv.matchTemplate(roi_gray, hunger_icon_img, cv.TM_CCOEFF_NORMED)
    threshold = 0.6
    _, max_val, _, _ = cv.minMaxLoc(res)
    # Zwróć True, jeśli najlepsze dopasowanie jest wystarczająco dobre
    return max_val >= threshold