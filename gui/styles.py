from tkinter import ttk


def set_dark_mode(root):
    background_color = '#333333'
    foreground_color = 'white'
    button_background = '#555555'
    table_row_background = '#a4e1b1'
    table_background = '#dbdada'
    button_foreground = 'white'
    select_background = '#444444'
    select_table_row_background = '#005577'

    # Ustawienie kolorów tła dla głównego okna
    root.configure(bg=background_color)

    style = ttk.Style()
    style.theme_create('darkmode', parent='alt',
                       settings={
                           'TNotebook': {
                               'configure': {
                                   'tabmargins': [2, 5, 2, 0],
                                   'background': background_color}
                           },
                           'TNotebook.Tab': {
                               'configure': {
                                   'padding': [5, 1],
                                   'background': button_background,
                                   'foreground': button_foreground},
                               'map': {
                                   'background': [
                                       ('selected', select_background)
                                   ],
                                   'expand': [
                                       ('selected', [1, 1, 1, 0])
                                   ]
                               }
                           },
                           'TFrame': {
                               'configure': {
                                   'background': background_color}
                           },
                           'TLabel': {
                               'configure': {
                                   'background': background_color,
                                   'foreground': foreground_color}
                           },
                           'TButton': {
                               'configure': {
                                   'background': button_background,
                                   'foreground': button_foreground,
                                   'borderwidth': 0},
                               'map': {
                                   'background': [
                                       ('active', select_background),
                                       ('pressed', select_background)
                                   ]
                               }
                           },
                           'Treeview': {
                               'configure': {
                                   'background': table_row_background,
                                   'fieldbackground': table_background,
                                   'foreground': 'black'},
                               'map': {
                                   'background': [
                                       ('selected', select_table_row_background)
                                   ]
                               }
                           },
                           'Treeview.Heading': {
                               'configure': {
                                   'background': '#b8b6b6',
                                   'foreground': 'black',
                                   'font': ('Helvetica', 10, 'bold')}
                           },
                           'Custom.TRadiobutton': {
                               'configure': {
                                   'background': background_color,
                                   'foreground': 'yellow',
                                   'bordercolor': 'blue',
                                   'lightcolor': 'green',
                                   'borderwidth': 1
                               },
                               'map': {
                                   'background': [
                                       ('selected', background_color),
                                       ('!selected', background_color)
                                   ],
                                   'indicatorcolor': [
                                       ('selected', 'blue'),
                                       ('!selected', 'white')
                                   ]
                               }
                           }
                       })
    style.theme_use('darkmode')

    # Aplikowanie stylów do innych widgetów poza ttk
    root.option_add("*Button.background", button_background)
    root.option_add("*Button.foreground", button_foreground)
    root.option_add("*Button.activeBackground", select_background)
    root.option_add("*Frame.background", background_color)
    root.option_add("*Label.background", background_color)
    root.option_add("*Radiobutton.background", background_color)
    root.option_add("*Label.foreground", foreground_color)
