import tkinter as tk
from tkinter import ttk
from config import api_get, api_post


def draw_profiles(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Profili")

    profili_notebook = ttk.Notebook(tab)
    profili_notebook.pack(fill='both', expand=True)

    def add_notebook_frame(notebook, text): #TODO sposta in funzioni varie
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=text)
        return frame

    profili_page = add_notebook_frame(profili_notebook, 'Profili')
    aree_page = add_notebook_frame(profili_notebook, 'Aree')
    listini_page = add_notebook_frame(profili_notebook, 'Listini')

    # profili_page
    profili_view = ttk.Frame(profili_page)
    profili_view.pack(fill='both', expand=True)

    # aree_page
    aree_view = ttk.Frame(aree_page)
    aree_view.pack(fill='both', expand=True)

    # listini_page
    listini_view = ttk.Frame(listini_page)
    listini_view.pack(fill='both', expand=True)

