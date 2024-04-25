from tkinter import filedialog


def save_hunting_points(hunting_steps):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            for key, value in hunting_steps.items():
                file.write(f"{key},{value[0]},{value[1]}\n")  # key, first value of tuple, second value of tuple


def load_hunting_points(table, hunting_steps):
    max_row_id = 0  # resetowanie max_row_id
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        hunting_steps.clear()  # Czyszczenie obecnego słownika
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                key = int(parts[0])
                value = (int(parts[1]), parts[2])
                hunting_steps[key] = value
                if key > max_row_id:
                    max_row_id = key  # aktualizowanie max_row_id do najwyższego klucza
        populate_table(table, hunting_steps)  # Aktualizacja tabeli po wczytaniu danych


def populate_table(table, hunting_steps):
    for i in table.get_children():
        table.delete(i)  # Czyszczenie istniejących danych w tabeli
    for key, (move_point, action) in hunting_steps.items():
        # Dodajemy wiersz używając klucza jako identyfikatora wiersza
        table.insert('', 'end', iid=key, values=(move_point, action))


def add_row(max_row_id, move_point_value, action_value, table, hunting_steps):
    max_row_id += 1
    # Pobranie wartości z radiobutton i listy
    selected_radio = move_point_value.get()
    selected_option = action_value.get()
    # Dodanie wartości do tabeli i słownika
    table.insert("", "end", iid=max_row_id, values=(selected_radio, selected_option))
    hunting_steps[max_row_id] = (selected_radio, selected_option)
    return max_row_id  # Zwracamy zaktualizowany max_row_id


def delete_row(table, hunting_steps):
    selected_item = table.selection()[0]  # Pobranie zaznaczonego wiersza
    if selected_item:  # Sprawdzenie, czy zaznaczono jakiś wiersz
        table.delete(selected_item)  # Usuwanie wiersza z tabeli
        del hunting_steps[int(selected_item)]  # Usuwanie wpisu ze słownika
    else:
        print("Nie zaznaczono żadnego wiersza")  # Informujemy, że nie zaznaczono wiersza
    print(hunting_steps)
