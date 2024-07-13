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
        super().__init__()
        self.title(f'Guarda Sagra - ' + profile['nome'])
        self.state('zoomed')  # Apre la finestra massimizzata
        self.draw_tabs(profile)  # TODO forse da rivedere
        self.create_menu()
        # self.menu = Menu(self)
        # self.frame1 = Frame1(self)

    def draw_tabs(self, profile):
        notebook = ttk.Notebook(self)

        if profile['privilegi'] % 2 == 0 or profile['privilegi'] == 1:
            cassa.draw_cassa(notebook, profile)
        if profile['privilegi'] % 3 == 0 or profile['privilegi'] == 1:
            pass  # Temporaneamente libero
        if profile['privilegi'] % 5 == 0 or profile['privilegi'] == 1:
            articoli.draw_articoli(notebook, profile)  #modifica listini, articoli e tipologie
        if profile['privilegi'] % 7 == 0 or profile['privilegi'] == 1:
            pass  # modifica profili, aree e listini collegati
        if profile['privilegi'] % 11 == 0 or profile['privilegi'] == 1:
            pass  # statistiche e report

        notebook.pack(expand=True, fill="both")

    def create_menu(self):
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label='New', command=lambda: print('New file'))
        file_menu.add_command(label='Open', command=lambda: print('Open file'))
        file_menu.add_separator()
        menu.add_cascade(label='File', menu=file_menu)
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