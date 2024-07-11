import tkinter as tk
from tkinter import ttk
import functools
import requests
import json

def draw_articoli(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Articoli")
    # definisco struttura-notebook principale
    articoli_notebook = ttk.Notebook(tab)
    articoli_notebook.pack(fill='both', expand=True)

    articoli_frame = ttk.Frame(articoli_notebook)
    articoli_notebook.add(articoli_frame, text='Articoli')

    tipologie_frame = ttk.Frame(articoli_notebook)
    articoli_notebook.add(tipologie_frame, text='Tipologie')

    listini_frame = ttk.Frame(articoli_notebook)
    articoli_notebook.add(listini_frame, text='Listini')

    # articoli_frame
