import cv2 as cv

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
import threading
import queue
import pytesseract

from config import IMAGE_PATHS_ICON_BUTTON_FIRST_ROW, IMAGE_PATHS_ICON_BUTTON_SECOND_ROW, NUMBER_OF_MONSTER_OPTIONS
from functionality_application.capture_frames import capture_frames
from functionality_game.hunting_point_table_operations import add_row, delete_row, load_hunting_points, \
    save_hunting_points
from functionality_game.process_control import start_mouse_listen, start_healing, stop_healing, start_hunting, \
    stop_hunting
from functionality_game.settings_manager import save_client_and_character_settings, load_client_and_character_settings
from gui.custom_widgets import MovementPointRadioButton
from gui.styles import set_dark_mode


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.cap = None
        self.camera_index = None
        self.is_auto_loot = tk.BooleanVar(value=False)
        self.number_of_monsters = tk.IntVar(value=1)
        self.is_hungry = tk.BooleanVar(value=False)
        self.hunting_steps = {}
        self.max_row_id = 0
        self.control_flags = {
            'running_HP_monitoring': False,
            'running_MANA_monitoring': False,
            'running_hunting': False,
            'index_move_point': 0
        }

        set_dark_mode(master)
        master.title("Tibia bot")
        master.geometry("800x600")

        self.notebook = ttk.Notebook(master)
        self.character_tab = tk.Frame(self.notebook)
        self.healing_tab = tk.Frame(self.notebook)
        self.hotkey_tab = tk.Frame(self.notebook)
        self.hunting_tab = tk.Frame(self.notebook)
        self.notebook.add(self.character_tab, text='Postać')
        self.notebook.add(self.healing_tab, text='Leczenie')
        self.notebook.add(self.hotkey_tab, text='Hotkey')
        self.notebook.add(self.hunting_tab, text='Hunting')
        self.notebook.pack(expand=1, fill="both")

        self.nested_notebook = ttk.Notebook(self.hunting_tab)
        self.nested_notebook.pack(expand=True, fill='both')

        # Stwórz zakładki dla zagnieżdżonego tabu 'hunting_tab'
        self.mapa_sub_tab_of_hunting_tab = ttk.Frame(self.nested_notebook)
        self.attack_sub_tab_of_hunting_tab = ttk.Frame(self.nested_notebook)
        self.support_sub_tab_of_hunting_tab = ttk.Frame(self.nested_notebook)

        self.nested_notebook.add(self.mapa_sub_tab_of_hunting_tab, text='Mapa')
        self.nested_notebook.add(self.attack_sub_tab_of_hunting_tab, text='Atakowanie')
        self.nested_notebook.add(self.support_sub_tab_of_hunting_tab, text='Wsparcie')

        self.label_character_name = tk.Label(
            self.character_tab,
            text="Nazwa postaci:"
        )
        self.label_character_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_character_name = tk.Entry(self.character_tab)
        self.entry_character_name.grid(row=0, column=1, padx=10, pady=10)
        self.character_name = tk.StringVar()
        self.entry_character_name.config(textvariable=self.character_name)

        self.btn_hp_tab_area = tk.Button(
            self.character_tab,
            text="Wybierz obszar tabu HP",
            command=lambda:
            start_mouse_listen(
                1,
                self.hp_area_coordinates,
                self.mana_area_coordinates,
                self.minimap_area_coordinates
            )
        )
        self.btn_hp_tab_area.grid(row=1, column=0, padx=10, pady=10)

        self.entry_hp_area_coordinates = tk.Entry(
            self.character_tab,
            state='readonly'
        )
        self.entry_hp_area_coordinates.grid(row=1, column=1, padx=10, pady=10)
        self.hp_area_coordinates = tk.StringVar()
        self.entry_hp_area_coordinates.config(textvariable=self.hp_area_coordinates)

        self.btn_mana_tab_area = tk.Button(
            self.character_tab,
            text="Wybierz obszar Tabu MANA",
            command=lambda:
            start_mouse_listen(
                1,
                self.hp_area_coordinates,
                self.mana_area_coordinates,
                self.minimap_area_coordinates
            )
        )
        self.btn_mana_tab_area.grid(row=2, column=0, padx=10, pady=10)

        self.entry_mana_area_coordinates = tk.Entry(
            self.character_tab,
            state='readonly'
        )
        self.entry_mana_area_coordinates.grid(row=2, column=1, padx=10, pady=10)
        self.mana_area_coordinates = tk.StringVar()
        self.entry_mana_area_coordinates.config(textvariable=self.mana_area_coordinates)

        self.btn_minimap_tab_area = tk.Button(
            self.character_tab,
            text="Wybierz obszar MiniMapy",
            command=lambda:
            start_mouse_listen(
                1,
                self.hp_area_coordinates,
                self.mana_area_coordinates,
                self.minimap_area_coordinates
            )
        )
        self.btn_minimap_tab_area.grid(row=3, column=0, padx=10, pady=10)
        self.entry_minimap_area_coordinates = tk.Entry(
            self.character_tab,
            state='readonly'
        )
        self.entry_minimap_area_coordinates.grid(row=3, column=1, padx=10, pady=10)
        self.minimap_area_coordinates = tk.StringVar()
        self.entry_minimap_area_coordinates.config(textvariable=self.minimap_area_coordinates)

        # Klaiwsz leczenia exura
        self.label_hotkey_heal_exura = tk.Label(
            self.hotkey_tab,
            text="Klawisz leczenia 'exura':"
        )
        self.label_hotkey_heal_exura.grid(row=0, column=2, padx=10, pady=10)
        self.entry_heal_key_exura = tk.Entry(
            self.healing_tab
        )
        self.entry_heal_key_exura.grid(row=0, column=3, padx=10, pady=10)
        self.heal_key_exura = tk.StringVar()
        self.entry_heal_key_exura.config(textvariable=self.heal_key_exura)

        # Klaiwsz leczenia exura gran
        self.label_hotkey_heal_exura_gran = tk.Label(
            self.hotkey_tab,
            text="Klawisz leczenia 'exura gran':"
        )
        self.label_hotkey_heal_exura_gran.grid(row=1, column=2, padx=10, pady=10)
        self.entry_heal_key_exura_gran = tk.Entry(
            self.hotkey_tab
        )
        self.entry_heal_key_exura_gran.grid(row=1, column=3, padx=10, pady=10)
        self.heal_key_exura_gran = tk.StringVar()
        self.entry_heal_key_exura_gran.config(textvariable=self.heal_key_exura_gran)

        # Klaiwsz spirit potion
        self.label_mana_spirit = tk.Label(
            self.hotkey_tab,
            text="Klawisz potion 'Spirit':"
        )
        self.label_mana_spirit.grid(row=2, column=2, padx=10, pady=10)
        self.entry_mana_key_spirit_potion = tk.Entry(
            self.healing_tab
        )
        self.entry_mana_key_spirit_potion.grid(row=2, column=3, padx=10, pady=10)
        self.mana_key_spirit_potion = tk.StringVar()
        self.entry_mana_key_spirit_potion.config(textvariable=self.mana_key_spirit_potion)

        self.label_hp_point_limit_exura = tk.Label(
            self.healing_tab,
            text="Lecz czarem 'exura' poniżej wartości:"
        )
        self.label_hp_point_limit_exura.grid(row=2, column=0, padx=10, pady=10)
        self.entry_hp_point_limit_exura = tk.Entry(self.healing_tab)
        self.entry_hp_point_limit_exura.grid(row=2, column=1, padx=10, pady=10)
        self.hp_point_limit_exura = tk.StringVar()
        self.entry_hp_point_limit_exura.config(textvariable=self.hp_point_limit_exura)

        self.hp_point_limit_exura_gran = tk.Label(
            self.healing_tab,
            text="Lecz czarem 'exura gran' poniżej wartości:"
        )
        self.hp_point_limit_exura_gran.grid(row=3, column=0, padx=10, pady=10)
        self.entry_hp_point_limit_exura_gran = tk.Entry(self.healing_tab)
        self.entry_hp_point_limit_exura_gran.grid(row=3, column=1, padx=10, pady=10)
        self.hp_point_limit_exura_gran = tk.StringVar()
        self.entry_hp_point_limit_exura_gran.config(textvariable=self.hp_point_limit_exura_gran)

        self.btn_save_settings = tk.Button(
            self.character_tab,
            text="Zapisz ustawienia",
            command=lambda:
            save_client_and_character_settings(
                self.character_name,
                self.hp_area_coordinates,
                self.mana_area_coordinates,
                self.minimap_area_coordinates,
                self.hp_point_limit_exura,
                self.hp_point_limit_exura_gran,
                self.heal_key_exura,
                self.heal_key_exura_gran,
                self.mana_key_spirit_potion
            )
        )
        self.btn_save_settings.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        load_client_and_character_settings(
            self.character_name,
            self.hp_area_coordinates,
            self.mana_area_coordinates,
            self.minimap_area_coordinates,
            self.hp_point_limit_exura,
            self.hp_point_limit_exura_gran,
            self.heal_key_exura,
            self.heal_key_exura_gran,
            self.mana_key_spirit_potion
        )

        self.btn_start_healing = tk.Button(
            self.character_tab,
            text="Start",
            bg="green",
            command=lambda:
            start_healing(
                self.cap,
                self.hp_area_coordinates,
                self.mana_area_coordinates,
                self.control_flags,
                self.frame_queue,
                self.hp_point_limit_exura,
                self.hp_point_limit_exura_gran,
                self.character_name,
                pytesseract
            )
        )
        self.btn_start_healing.grid(row=5, column=0, padx=10, pady=10)

        self.btn_stop_healing = tk.Button(
            self.character_tab,
            text="Stop",
            bg="red",
            command=lambda:
            stop_healing(
                self.control_flags
            )
        )
        self.btn_stop_healing.grid(row=5, column=1, padx=10, pady=10)

        # Zmienne dla radiobutton i opcji z listy
        self.move_point_value = tk.IntVar(value=1)
        self.action_value = tk.StringVar(value="MOVE")

        # Tworzenie kontenerów dla rzędów w 'mapa_sub_tab_of_hunting_tab'
        mapa_sub_tab_row_1 = tk.Frame(self.mapa_sub_tab_of_hunting_tab)
        mapa_sub_tab_row_1.pack(fill=tk.X, padx=5, pady=5)

        mapa_sub_tab_row_2 = tk.Frame(self.mapa_sub_tab_of_hunting_tab)
        mapa_sub_tab_row_2.pack(fill=tk.X, padx=5, pady=5)

        mapa_sub_tab_row_3 = tk.Frame(self.mapa_sub_tab_of_hunting_tab)
        mapa_sub_tab_row_3.pack(fill=tk.X, padx=5, pady=5)

        mapa_sub_tab_row_4 = tk.Frame(self.mapa_sub_tab_of_hunting_tab)
        mapa_sub_tab_row_4.pack(fill=tk.X, padx=5, pady=5)

        mapa_sub_tab_row_5 = tk.Frame(self.mapa_sub_tab_of_hunting_tab)
        mapa_sub_tab_row_5.pack(fill=tk.X, padx=5, pady=5)

        custom_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        point_map_label = tk.Label(
            mapa_sub_tab_row_1,
            text="Zdefiniuj punkty mapy",
            font=custom_font
        )
        point_map_label.pack(side='left', anchor='n', pady=10)

        for img_path, value in IMAGE_PATHS_ICON_BUTTON_FIRST_ROW:
            img_checkbox = MovementPointRadioButton(mapa_sub_tab_row_2, img_path, self.move_point_value, value, self)
            img_checkbox.pack(side=tk.LEFT, padx=5, anchor='n')  # Umieszczanie poziomo z przerwami i na górze

        for img_path, value in IMAGE_PATHS_ICON_BUTTON_SECOND_ROW:
            img_checkbox = MovementPointRadioButton(mapa_sub_tab_row_3, img_path, self.move_point_value, value, self)
            img_checkbox.pack(side=tk.LEFT, padx=5, pady=5, anchor='n')  # Umieszczanie poziomo z przerwami i na górze

        option_menu_label = ttk.Label(
            mapa_sub_tab_row_2,
            text="Wybierz czynność:"
        )
        option_menu_label.pack(side='left', padx=10)

        option_menu_list = ttk.Combobox(
            mapa_sub_tab_row_2,
            textvariable=self.action_value,
            values=["MOVE", "ROPE", "HOLE", "STAIRS"],
            state='readonly',
            width=10
        )
        option_menu_list.pack(side='left', padx=10)

        auto_loot_label = ttk.Label(
            mapa_sub_tab_row_3,
            text="Auto loot:"
        )
        auto_loot_label.pack(side='left', padx=10)

        self.switch_auto_loot = tk.Checkbutton(
            mapa_sub_tab_row_3,
            variable=self.is_auto_loot,
            onvalue=True,
            offvalue=False
        )
        self.switch_auto_loot.pack(side='left', padx=10)

        row_attack_sub_tab_1 = tk.Frame(self.attack_sub_tab_of_hunting_tab)
        row_attack_sub_tab_1.pack(fill=tk.X, padx=5, pady=5)
        row_attack_sub_tab_2 = tk.Frame(self.attack_sub_tab_of_hunting_tab)
        row_attack_sub_tab_2.pack(fill=tk.X, padx=5, pady=5)

        number_of_monsters_label = ttk.Label(
            row_attack_sub_tab_1,
            text="Wybierz liczbę potworów:"
        )
        number_of_monsters_label.pack(side='left', padx=10)

        number_of_monsters_option = ttk.Combobox(
            row_attack_sub_tab_1,
            textvariable=self.number_of_monsters,
            values=NUMBER_OF_MONSTER_OPTIONS,
            state='readonly',
            width=10
        )
        number_of_monsters_option.pack(side='left', padx=10)

        row_support_sub_tab_1 = tk.Frame(self.support_sub_tab_of_hunting_tab)
        row_support_sub_tab_1.pack(fill=tk.X, padx=5, pady=5)
        row_support_sub_tab_2 = tk.Frame(self.support_sub_tab_of_hunting_tab)
        row_support_sub_tab_2.pack(fill=tk.X, padx=5, pady=5)

        self.switch_auto_eat = tk.Checkbutton(
            row_support_sub_tab_1,
            text="Jedzenie",
            variable=self.is_hungry,
            onvalue=True,
            offvalue=False
        )
        self.switch_auto_eat.pack(side='left', padx=10)

        self.switch_auto_haste = tk.Checkbutton(
            row_support_sub_tab_2,
            text="Auto Haste",
            onvalue=True,
            offvalue=False
        )
        self.switch_auto_haste.pack(side='left', padx=10)

        # Tabela do wyświetlania danych
        columns = ("radiobutton_value", "list_value")
        self.table = ttk.Treeview(
            mapa_sub_tab_row_5,
            columns=columns,
            show="headings"
        )
        self.table.heading("radiobutton_value", text="Wartość punktu")
        self.table.heading("list_value", text="Czynność")
        self.table.pack(side='top', fill='both', expand=True)

        vscroll = ttk.Scrollbar(
            mapa_sub_tab_row_5,
            orient=tk.VERTICAL,
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=vscroll.set)
        vscroll.pack(side=tk.LEFT, fill=tk.Y)
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        add_hunting_point_button = tk.Button(
            mapa_sub_tab_row_5,
            text="Dodaj punkt",
            command=lambda: setattr(
                self,
                'max_row_id',
                add_row(
                    self.max_row_id,
                    self.move_point_value,
                    self.action_value,
                    self.table,
                    self.hunting_steps
                )
            )
        )
        add_hunting_point_button.pack(side='top', fill='x')

        delete_hunting_point_button = tk.Button(
            mapa_sub_tab_row_5,
            text="Usuń punkt",
            command=lambda:
            delete_row(
                self.table,
                self.hunting_steps
            )
        )
        delete_hunting_point_button.pack(side='top', fill='x')

        self.save_button = tk.Button(
            mapa_sub_tab_row_5,
            text="Zapisz punkty",
            command=lambda:
            save_hunting_points(
                self.hunting_steps
            )
        )
        self.save_button.pack(side='top', fill='x')

        self.load_button = tk.Button(
            mapa_sub_tab_row_5,
            text="Wczytaj punkty",
            command=lambda:
            load_hunting_points(
                self.table,
                self.hunting_steps
            )
        )
        self.load_button.pack(side='top', fill='x')
        self.frame_queue = queue.Queue(maxsize=30)  # Ustawienie maksymalnego rozmiaru kolejki
        btn_start_hunting = tk.Button(
            self.hunting_tab,
            text="Start",
            bg="green",
            command=lambda:
                start_hunting(
                    self.cap,
                    self.minimap_area_coordinates,
                    self.control_flags,
                    self.hunting_steps,
                    self.number_of_monsters,
                    self.character_name,
                    self.is_auto_loot,
                    self.frame_queue,
                    self.is_hungry
                )
        )
        btn_start_hunting.pack(side='left', anchor='n', pady=10)

        btn_stop_hunting = tk.Button(self.hunting_tab, text="Stop", bg="red",
                                     command=lambda: stop_hunting(self.control_flags))
        btn_stop_hunting.pack(side='left', anchor='n', pady=10)

        self.camera_index = 1
        self.cap = cv.VideoCapture(self.camera_index, cv.CAP_DSHOW)  # Inicjalizacja kamery
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

        # Uruchomienie wątku do przechwytywania ramek
        self.capture_thread = threading.Thread(target=capture_frames, args=(self.cap, self.frame_queue), daemon=True)
        self.capture_thread.start()
