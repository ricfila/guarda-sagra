import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, colorchooser
import requests
import json
from config import api_get, api_post

def on_tipologie_select(event, tipologie):
    pass

def draw_articoli(notebook, profile):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Articoli")

    # definisco struttura-notebook principale
    articoli_notebook = ttk.Notebook(tab)
    articoli_notebook.pack(fill='both', expand=True)

    def add_notebook_frame(notebook, text):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=text)
        return frame

    articoli_frame = add_notebook_frame(articoli_notebook, 'Articoli')
    tipologie_frame = add_notebook_frame(articoli_notebook, 'Tipologie')
    listini_frame = add_notebook_frame(articoli_notebook, 'Listini')

    # articoli_frame
    # tipologie_frame
    tipologie_view = ttk.Frame(tipologie_frame)
    tipologie_view.pack(side='left', fill='both', expand=True)

    tipologie = ttk.Treeview(tipologie_view, columns=('nome', 'sfondo', 'id', 'posizione', 'visibile'),
                          show='headings')
    tipologie.heading('id', text='')
    tipologie.heading('nome', text='Nome tipologia')
    tipologie.heading('posizione', text='')
    tipologie.heading('sfondo', text='Colore sfondo')
    tipologie.heading('visibile', text='')

    tipologie.column('id', width=0)
    tipologie.column('nome', width=1000)  # width molto alta per occupare tutto lo
    tipologie.column('posizione', width=0)
    tipologie.column('sfondo', width=1000)
    tipologie.column('visibile', width=0)

    tipologie.pack(side='left', fill='both', expand=True)

    tipologie.bind("<Button-1>", lambda event, tip=tipologie: on_tipologie_select(event, tip))

    for item in api_get('/tipologie'):
        tipologie.insert('', 'end',
                        values=(item['nome'], item['sfondo'], item['id'], item['posizione'], item['visibile']))



    def choose_color():
        color = colorchooser.askcolor()[1]  # Returns (color_rgb, color_name)
        return color
    # listini_frame
