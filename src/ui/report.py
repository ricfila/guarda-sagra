import tkinter as tk
from tkinter import ttk
from .funzioni_generiche import api_get, api_post

def get_report():
    pass #TODO

def draw_report(notebook):
    tab_report = ttk.Frame(notebook)
    notebook.add(tab_report, text="Report")

    columns = get_report()

    #report_treeview = ttk.Treeview(tab_report, columns=columns, show='headings')

    #for column in columns:
    #    report_treeview.heading ('nome_colonna', text = 'Nome colonna')

    #report_treeview.pack()

