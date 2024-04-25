from config import CLIENT_AND_CHARACTER_FILE_SETTINGS


def save_client_and_character_settings(character_name, hp_area_coordinates, mana_area_coordinates,
                                       minimap_area_coordinates, hp_point_limit, mana_point_limit,
                                       heal_key_exura, heal_key_exura_gran, mana_key_spirit_potion):
    with open(CLIENT_AND_CHARACTER_FILE_SETTINGS, "w") as plik:
        plik.write(f"Nazwa postaci: {character_name.get()}\n")
        plik.write(f"Obszar tabu HP: {hp_area_coordinates.get()}\n")
        plik.write(f"Obszar tabu MANA: {mana_area_coordinates.get()}\n")
        plik.write(f"Obszar MiniMapy: {minimap_area_coordinates.get()}\n")
        plik.write(f"Leczenie exura poniżej: {hp_point_limit.get()}\n")
        plik.write(f"Leczenie exura gran poniżej: {mana_point_limit.get()}\n")
        plik.write(f"Klawisz leczenia exura: {heal_key_exura.get()}\n")
        plik.write(f"Klawisz leczenia exura gran: {heal_key_exura_gran.get()}\n")
        plik.write(f"Klawisz spirit potion: {mana_key_spirit_potion.get()}\n")


def load_client_and_character_settings(character_name, hp_area_coordinates, mana_area_coordinates,
                                       minimap_area_coordinates, hp_point_limit, mana_point_limit,
                                       heal_key_exura, heal_key_exura_gran, mana_key_spirit_potion):
    try:
        with open(CLIENT_AND_CHARACTER_FILE_SETTINGS, "r") as plik:
            linie = plik.readlines()
            if len(linie) > 0:
                character_name.set(linie[0].split(": ")[1].strip())
            if len(linie) > 1:
                # Usuń etykietę i białe znaki, zachowaj tylko współrzędne
                hp_area_coordinates_str = linie[1].split(": ")[1].strip()
                hp_area_coordinates.set(hp_area_coordinates_str)

            if len(linie) > 2:
                mana_area_coordinates_str = linie[2].split(": ")[1].strip()
                mana_area_coordinates.set(mana_area_coordinates_str)

            if len(linie) > 3:
                minimap_area_coordinates_str = linie[3].split(": ")[1].strip()
                minimap_area_coordinates.set(minimap_area_coordinates_str)

            if len(linie) > 4:
                hp_point_limit.set(linie[4].split(": ")[1].strip())
            if len(linie) > 5:
                mana_point_limit.set(linie[5].split(": ")[1].strip())
            if len(linie) > 6:
                heal_key_exura.set(linie[6].split(": ")[1].strip())
            if len(linie) > 7:
                heal_key_exura_gran.set(linie[7].split(": ")[1].strip())
            if len(linie) > 8:
                mana_key_spirit_potion.set(linie[8].split(": ")[1].strip())

    except FileNotFoundError:
        pass  # Jeśli plik nie istnieje, to nic nie rób
