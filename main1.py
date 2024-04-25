import tkinter as tk
from tkinter import ttk


def add_row():
    global max_row_id
    # Increment the max_row_id for each new row
    max_row_id += 1
    selected_radio = radio_value.get()
    selected_option = option_value.get()
    table.insert("", "end", iid=max_row_id, values=(selected_radio, selected_option))
    data_dict[max_row_id] = (selected_radio, selected_option)


# Initialize a variable to keep track of the highest assigned row_id
max_row_id = 0


def delete_row():
    selected_items = table.selection()
    if selected_items:  # Sprawdzamy, czy jakiś element jest zaznaczony
        selected_item = selected_items[0]  # Zaznaczamy pierwszy wybrany element
        table.delete(selected_item)  # Usuwamy zaznaczony wiersz z tabeli
        del data_dict[int(selected_item)]  # Usuwamy z słownika
    else:
        print("Nie zaznaczono żadnego wiersza")  # Informujemy, że nie zaznaczono wiersza
    print(data_dict)
    # Inicjalizacja głównego okna


root = tk.Tk()
root.title("Aplikacja z Radiobutton i Listą")

# Słownik do przechowywania danych z tabeli
data_dict = {}

# Zmienne dla radiobutton i opcji z listy
radio_value = tk.IntVar(value=1)
option_value = tk.StringVar(value="MOVE")

# Radiobuttons
for i in range(1, 6):
    radio_button = tk.Radiobutton(root, text=str(i), variable=radio_value, value=i)
    radio_button.pack(side='top', fill='x')

# Dropdown list
option_menu = ttk.Combobox(root, textvariable=option_value, values=["MOVE"])
option_menu.pack(side='top', fill='x')

# Przycisk do dodawania wierszy
add_button = tk.Button(root, text="Dodaj wiersz", command=add_row)
add_button.pack(side='top', fill='x')

# Tabela do wyświetlania danych
columns = ("radiobutton_value", "list_value")
table = ttk.Treeview(root, columns=columns, show="headings")
table.heading("radiobutton_value", text="Wartość z Radiobutton")
table.heading("list_value", text="Wartość z Listy")
table.pack(side='top', fill='both', expand=True)

# Przycisk do usuwania wierszy
delete_button = tk.Button(root, text="Usuń wiersz", command=delete_row)
delete_button.pack(side='top', fill='x')

# Uruchomienie głównej pętli aplikacji
root.mainloop()
