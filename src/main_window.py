import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
import sys  # used to end the program
import config
class Main_window(tk.Tk):
    def __init__(self, profile):
        print(profile) #TODO inserire le modifiche date dalla scelta profilo
        super().__init__()
        self.title('Guarda Sagra')
        self.state('zoomed') # Apre la finestra massimizzata
        self.draw_notebook(profile) # TODO forse da rivedere
        # self.menu = Menu(self)
        # self.frame1 = Frame1(self)

    def draw_notebook(self, profile):
        notebook = ttk.Notebook(self)
        #TODO inserisci quì parti condivise tra tutti i profili
        #TODO parte_condivisa = self.create_tab(notebook, "Condivisa")
        if profile == 'Admin':
            tab_listini = self.create_tab(notebook, "Listini")
            esempio_label1 = ttk.Label(tab_listini, text='Aperto il tab listini')
            esempio_label1.pack()

            tab_ingredienti = self.create_tab(notebook, "Ingredienti")
            esempio_label2 = ttk.Label(tab_ingredienti, text='Aperto il tab ingredienti')
            esempio_label2.pack()

            tab_tipologie = self.create_tab(notebook, "Tipologie")
            esempio_label3 = ttk.Label(tab_tipologie, text='Aperto il tab Tipologie')
            esempio_label3.pack()

            tab_sconti = self.create_tab(notebook, "Sconti")
            esempio_label4 = ttk.Label(tab_sconti, text='Aperto il tab Sconti')
            esempio_label4.pack()

            tab_profili = self.create_tab(notebook, "Profili")
            esempio_label5 = ttk.Label(tab_profili, text='Aperto il tab Profili')
            esempio_label5.pack()

            tab_stati = self.create_tab(notebook, "Stati")
            esempio_label6 = ttk.Label(tab_stati, text='Aperto il tab Stati')
            esempio_label6.pack()

            tab_tipo_pagamento = self.create_tab(notebook, "Tipo Pagamento")
            esempio_label7 = ttk.Label(tab_tipo_pagamento, text='Aperto il tab Tipo Pagamento')
            esempio_label7.pack()

            tab_statistiche_generali = self.create_tab(notebook, "Statistiche Generali")
            esempio_label8 = ttk.Label(tab_statistiche_generali, text='Aperto il tab Statistiche Generali')
            esempio_label8.pack()
        else:
            tab_avanzamento_stati = self.create_tab(notebook, "Avanzamento Stati")
            esempio_label1 = ttk.Label(tab_avanzamento_stati, text='Aperto il tab Avanzamento Stati')
            esempio_label1.pack()

            # Example 2: Scorte
            tab_scorte = self.create_tab(notebook, "Scorte")
            esempio_label2 = ttk.Label(tab_scorte, text='Aperto il tab Scorte')
            esempio_label2.pack()

            # Example 3: Chiusura Cassa
            tab_chiusura_cassa = self.create_tab(notebook, "Chiusura Cassa")
            esempio_label3 = ttk.Label(tab_chiusura_cassa, text='Aperto il tab Chiusura Cassa')
            esempio_label3.pack()

        notebook.pack(expand=True, fill="both")

    def create_tab(self, notebook, title):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=title)
        return tab


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