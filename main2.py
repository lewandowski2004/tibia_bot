# Tworzenie kontenerów dla rzędów
row1 = tk.Frame(self.mapa_sub_tab_of_hunting_tab)
row1.pack(fill=tk.X, padx=5, pady=5)

row2 = tk.Frame(self.mapa_sub_tab_of_hunting_tab)
row2.pack(fill=tk.X, padx=5, pady=5)
# Używamy fill=tk.X, aby rozciągnąć ramkę w poziomie

row3 = tk.Frame(self.mapa_sub_tab_of_hunting_tab)
row3.pack(fill=tk.X, padx=5, pady=5)

row4 = tk.Frame(self.mapa_sub_tab_of_hunting_tab)
row4.pack(fill=tk.X, padx=5, pady=5)

row5 = tk.Frame(self.mapa_sub_tab_of_hunting_tab)
row5.pack(fill=tk.X, padx=5, pady=5)

# Definiowanie czcionki
custom_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

# Tworzenie etykiety
label = tk.Label(self.mapa_sub_tab_of_hunting_tab, text="Zdefiniuj punkty mapy", font=custom_font)
label.grid(row=0, column=0, padx=10, pady=10)

for img_path, value in IMAGE_PATHS_ICON_BUTTON_FIRST_ROW:
    img_checkbox = MovementPointRadioButton(row2, img_path, self.move_point_value, value, self)
    img_checkbox.pack(side=tk.LEFT, padx=5, anchor='n')  # Umieszczanie poziomo z przerwami i na górze

for img_path, value in IMAGE_PATHS_ICON_BUTTON_SECOND_ROW:
    img_checkbox = MovementPointRadioButton(row3, img_path, self.move_point_value, value, self)
    img_checkbox.pack(side=tk.LEFT, padx=5, pady=5, anchor='n')  # Umieszczanie poziomo z przerwami i na górze

# Utworzenie etykiety i umieszczenie jej po lewej stronie Combobox
label = ttk.Label(row2, text="Wybierz czynność:")
label.pack(side='left', padx=10)

# Dropdown list
option_menu = ttk.Combobox(row2, textvariable=self.action_value, values=["MOVE", "ROPE", "HOLE", "STAIRS"],
                           state='readonly', width=10)
option_menu.pack(side='left', padx=10)

self.is_auto_loot = tk.BooleanVar(value=False)
label = ttk.Label(row3, text="Auto loot:")
label.pack(side='left', padx=10)
self.switch_auto_loot = tk.Checkbutton(row3,
                                       var=self.is_auto_loot,
                                       onvalue=True, offvalue=False)
self.switch_auto_loot.pack(side='left', padx=10)

row_attack_1 = tk.Frame(self.attack_sub_tab_of_hunting_tab)
row_attack_1.pack(fill=tk.X, padx=5, pady=5)
row_attack_2 = tk.Frame(self.attack_sub_tab_of_hunting_tab)
row_attack_2.pack(fill=tk.X, padx=5, pady=5)

label = ttk.Label(row_attack_1, text="Wybierz liczbę potworów:")
label.pack(side='left', padx=10)

self.number_of_monsters = tk.IntVar(value=1)
# Dropdown list
number_of_monsters_option = ttk.Combobox(row_attack_1, textvariable=self.number_of_monsters,
                                         values=["1", "2", "3", "4"],
                                         state='readonly', width=10)
number_of_monsters_option.pack(side='left', padx=10)

self.is_hungry = tk.BooleanVar(value=False)

row_support_1 = tk.Frame(self.support_sub_tab_of_hunting_tab)
row_support_1.pack(fill=tk.X, padx=5, pady=5)
row_support_2 = tk.Frame(self.support_sub_tab_of_hunting_tab)
row_support_2.pack(fill=tk.X, padx=5, pady=5)

self.switch = tk.Checkbutton(row_support_1, text="Jedzenie",
                             var=self.is_hungry,
                             onvalue=True, offvalue=False)
self.switch.pack(side='left', padx=10)

self.switch_auto_haste = tk.Checkbutton(row_support_2, text="Auto Haste",
                                        onvalue=True, offvalue=False)
self.switch_auto_haste.pack(side='left', padx=10)

# Tabela do wyświetlania danych
columns = ("radiobutton_value", "list_value")
self.table = ttk.Treeview(row5, columns=columns, show="headings")
self.table.heading("radiobutton_value", text="Wartość punktu")
self.table.heading("list_value", text="Czynność")
self.table.pack(side='top', fill='both', expand=True)
# Utwórz pionowy scrollbar i skonfiguruj go
vscroll = ttk.Scrollbar(row5, orient=tk.VERTICAL, command=self.table.yview)
self.table.configure(yscrollcommand=vscroll.set)
vscroll.pack(side=tk.LEFT, fill=tk.Y)
# Dodaj Treeview do ramki
self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Przycisk do dodawania kroków drogi
add_hunting_point_button = tk.Button(
    row5,
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

# Przycisk do usuwania kroków drogi
delete_hunting_point_button = tk.Button(
    row5,
    text="Usuń punkt",
    command=lambda:
    delete_row(
        self.table,
        self.hunting_steps
    )
)
delete_hunting_point_button.pack(side='top', fill='x')

self.save_button = tk.Button(
    row5,
    text="Zapisz punkty",
    command=lambda:
    save_hunting_points(
        self.hunting_steps
    )
)
self.save_button.pack(side='top', fill='x')

self.load_button = tk.Button(
    row5,
    text="Wczytaj punkty",
    command=lambda:
    load_hunting_points(
        self.table,
        self.hunting_steps
    )
)
self.load_button.pack(side='top', fill='x')
self.frame_queue = queue.Queue(maxsize=30)  # Ustawienie maksymalnego rozmiaru kolejki
btn_start_hunting = tk.Button(self.hunting_tab, text="Start", bg="green",
                              command=lambda: start_hunting(self.cap, self.wspolrzedne3, self.control_flags,
                                                            self.hunting_steps, self.number_of_monsters,
                                                            self.character_name, self.is_auto_loot,
                                                            self.frame_queue, self.is_hungry))
btn_start_hunting.pack(side='left', anchor='n', pady=10)

btn_stop_hunting = tk.Button(self.hunting_tab, text="Stop", bg="red", command=lambda: stop_hunting(self.control_flags))
btn_stop_hunting.pack(side='left', anchor='n', pady=10)

self.camera_index = 1
self.cap = cv.VideoCapture(self.camera_index, cv.CAP_DSHOW)  # Inicjalizacja kamery
self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

# Uruchomienie wątku do przechwytywania ramek
self.capture_thread = threading.Thread(target=capture_frames, args=(self.cap, self.frame_queue), daemon=True)
self.capture_thread.start()
