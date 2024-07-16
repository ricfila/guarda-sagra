import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
import sys  # used to end the program
import config
from ui import *
class Main_window(tk.Tk):
    def __init__(self, profile, logout_value):
        super().__init__()
        self.title(f'Guarda Sagra - ' + profile['nome'])
        self.state('zoomed')  # Apre la finestra massimizzata
        self.draw_tabs(profile)  # TODO forse da rivedere
        self.create_menu(logout_value)
        # self.menu = Menu(self)
        # self.frame1 = Frame1(self)

    def draw_tabs(self, profile):
        notebook = ttk.Notebook(self)

        if profile['privilegi'] == 1 or profile['privilegi'] % 2 == 0:
            cassa.draw_cassa(notebook, profile)
        if profile['privilegi'] == 1 or profile['privilegi'] % 3 == 0:
            pass  # Temporaneamente libero
        if profile['privilegi'] == 1 or profile['privilegi'] % 5 == 0:
            articoli.draw_articoli(notebook, profile)  # modifica listini, articoli e tipologie
        if profile['privilegi'] == 1 or profile['privilegi'] % 7 == 0:
            profili.draw_profiles(notebook)  # modifica profili, aree e listini collegati
        if profile['privilegi'] == 1 or profile['privilegi'] % 11 == 0:
            report.draw_report(notebook)

        notebook.pack(expand=True, fill="both")

    def create_menu(self, logout_value):
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label='Logout', command=lambda: logout(self, logout_value))
        file_menu.add_separator()
        menu.add_cascade(label='File', menu=file_menu)
        self.configure(menu=menu)
def logout(self, logout_value):
    logout_value.set(True)
    self.destroy()
