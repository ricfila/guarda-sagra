import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
import sys  # used to end the program
import config
from ui.tabs import *
class Main_window(tk.Tk):
    def __init__(self, profile):
        print(profile) #TODO inserire le modifiche date dalla scelta profilo
        super().__init__()
        self.title(f'Guarda Sagra - ' + profile)
        self.state('zoomed') # Apre la finestra massimizzata
        self.draw_tabs(profile) # TODO forse da rivedere
        self.create_menu()
        # self.menu = Menu(self)
        # self.frame1 = Frame1(self)

    def draw_tabs(self, profile):
        notebook = ttk.Notebook(self)
        #TODO inserisci quì parti condivise tra tutti i profili
        #TODO parte_condivisa = self.create_tab(notebook, "Condivisa")

        # Schermate condivise tra tutti i profili
        cassa.draw_cassa(notebook)
        '''
        if profile == 'Admin':
            self.draw_tab(notebook, "Listini")
            self.draw_tab(notebook, "Ingredienti")
            self.draw_tab(notebook, "Tipologie")
            self.draw_tab(notebook, "Sconti")
            self.draw_tab(notebook, "Profili")
            self.draw_tab(notebook, "Stati")
            self.draw_tab(notebook, "Tipo Pagamento")
            self.draw_tab(notebook, "Statistiche Generali")
        else:
            self.draw_tab(notebook, "Avanzamento Stati")
            self.draw_tab(notebook, "Scorte")
            self.draw_tab(notebook, "Chiusura Cassa")
        '''
        notebook.pack(expand=True, fill="both")

    def create_menu(self):
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label='New', command=lambda: print('New file'))
        file_menu.add_command(label='Open', command=lambda: print('Open file'))
        file_menu.add_separator()
        menu.add_cascade(label='File', menu=file_menu)
        '''
        # another sub menu
        help_menu = tk.Menu(menu, tearoff=False)
        help_menu.add_command(label='Help entry', command=lambda: print(help_check_string.get()))

        help_check_string = tk.StringVar()
        help_menu.add_checkbutton(label='check', onvalue='on', offvalue='off', variable=help_check_string)

        menu.add_cascade(label='Help', menu=help_menu)

        # add another menu to the main menu, this one should have a sub menu
        # try to read the website below and add a submenu
        # docs: https://www.tutorialspoint.com/python/tk_menu.htm
        exercise_menu = tk.Menu(menu, tearoff=False)
        exercise_menu.add_command(label='exercise test 1')
        menu.add_cascade(label='Exercise', menu=exercise_menu)

        exercise_sub_menu = tk.Menu(menu, tearoff=False)
        exercise_sub_menu.add_command(label='some more stuff')
        exercise_menu.add_cascade(label='more stuff', menu=exercise_sub_menu)
        '''
        self.configure(menu=menu)

class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=0.3, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        # create the widgets
        menu_button1 = ttk.Button(self, text='Button 1')
        menu_button2 = ttk.Button(self, text='Button 2')
        menu_button3 = ttk.Button(self, text='Button 3')

        menu_slider1 = ttk.Scale(self, orient='vertical')
        menu_slider2 = ttk.Scale(self, orient='vertical')

        toggle_frame = ttk.Frame(self)
        menu_toggle1 = ttk.Checkbutton(toggle_frame, text='check 1')
        menu_toggle2 = ttk.Checkbutton(toggle_frame, text='check 2')

        entry = ttk.Entry(self)

        # create the grid
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        # place the widgets
        menu_button1.grid(row=0, column=0, sticky='nswe', columnspan=2)
        menu_button2.grid(row=0, column=2, sticky='nswe')
        menu_button3.grid(row=1, column=0, columnspan=3, sticky='nsew')

        menu_slider1.grid(row=2, column=0, rowspan=2, sticky='nsew', pady=20)
        menu_slider2.grid(row=2, column=2, rowspan=2, sticky='nsew', pady=20)

        # toggle layout
        toggle_frame.grid(row=4, column=0, columnspan=3, sticky='nsew')
        menu_toggle1.pack(side='left', expand=True)
        menu_toggle2.pack(side='left', expand=True)

        # entry layout
        entry.place(relx=0.5, rely=0.95, relwidth=0.9, anchor='center')


class Frame1(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.3, y=0, relwidth=0.7, relheight=1)
        Entry(self, 'Entry 1', 'Button 1', 'green')
        Entry(self, 'Entry 2', 'Button 2', 'blue')
        Entry(self, 'Entry 3', 'Button 3', 'green')


class Entry(ttk.Frame):
    def __init__(self, parent, label_text, button_text, label_background):
        super().__init__(parent)

        label = ttk.Label(self, text=label_text, background=label_background)
        button = ttk.Button(self, text=button_text)

        label.pack(expand=True, fill='both')
        button.pack(expand=True, fill='both', pady=10)

        self.pack(side='left', expand=True, fill='both', padx=20, pady=20)