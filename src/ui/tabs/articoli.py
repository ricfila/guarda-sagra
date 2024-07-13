import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, colorchooser
import requests
import json
from config import api_get, api_post

def on_tipologie_select(event, treeview): #TODO unisci a on_select di cassa.py e sposta in modulo per funzioni generiche
    region = treeview.identify("region", event.x, event.y)
    if region == "cell":
        indice_colonna = treeview.identify_column(event.x)
        nome_colonna = treeview.column(indice_colonna)['id']
        id_riga = treeview.identify_row(event.y)
        if nome_colonna == 'nome':
            on_select_modifica(treeview, id_riga, indice_colonna, nome_colonna)
        if nome_colonna == 'sfondo':
            on_select_colore(treeview, id_riga, nome_colonna)

        elif nome_colonna == 'rimuovi':
            on_select_rimuovi(treeview, id_riga)

def on_select_colore(treeview, id_riga, nome_colonna):
    def scelta_colore():
        colore = colorchooser.askcolor(title = "Scelta dello sfondo per la tipologia "+ treeview.item(id_riga, 'values')[1])[1]
        return colore  #  '#hex' (es: '#000000')

    colore = scelta_colore()
    treeview.set(id_riga, nome_colonna, colore)
    refresh_colori(treeview)

def refresh_colori(treeview):
    for riga in treeview.get_children():
        colore = treeview.item(riga, 'values')[2]
        if colore != 'None':
            nome_tag = treeview.item(riga, 'values')[1].replace(' ', '_') + '_colore'
            treeview.tag_configure(nome_tag, background=colore)
            treeview.item(riga, tags=nome_tag)


def on_select_modifica(treeview, id_riga, indice_colonna, nome_colonna):
    # click sinistro per modificare note. "invio" o click fuori per modificare, "esc" per annullare
    bbox = treeview.bbox(id_riga, nome_colonna)

    if bbox:
        x, y, width, height = bbox
        valori_riga_attuali = treeview.item(id_riga, 'values')[int(indice_colonna[1:])-1]
        entry_per_modifica = ttk.Entry(treeview, width=width)
        entry_per_modifica.insert(0, valori_riga_attuali)

        def save_edit(event):
            new_value = entry_per_modifica.get()
            treeview.set(id_riga, nome_colonna, new_value)
            entry_per_modifica.destroy()

        entry_per_modifica.bind("<Return>", save_edit) # invio
        entry_per_modifica.bind("<FocusOut>", save_edit)  # se si vuole eliminare la modifica clickando al di fuori, modifica in cancel_edit

        def cancel_edit(event):
            entry_per_modifica.destroy()
            treeview.set(id_riga, nome_colonna, valori_riga_attuali)


        entry_per_modifica.bind("<Escape>", cancel_edit)

        entry_per_modifica.place(x=x, y=y, width=width, height=height)
        entry_per_modifica.update_idletasks()
        def set_focus():
            entry_per_modifica.focus_set()
        entry_per_modifica.after_idle(set_focus)

def on_select_rimuovi(treeview, id_riga):
    reply = messagebox.askquestion("Elimina tipologia", f"Vuoi eliminare la tipologia " + treeview.item(id_riga, 'values')[1])
    if reply == 'yes':
        #TODO DELETE REQUEST API
        treeview.delete(id_riga)

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
    def add_tipologia(tipologie):
        pass
    # TODO aggiungi label e entry per nome, posizione e sfondo. bottone per settare colore, poi click su aggiungi
    #  per aggiungere. deve calcolare l'id massimo e fare +1
    aggiungi_tipologia = ttk.Button(tipologie_view, text="Aggiungi tipologia", command=add_tipologia(tipologie))


    tipologie = ttk.Treeview(tipologie_view, columns=('rimuovi', 'nome', 'sfondo', 'id', 'posizione', 'visibile'),
                          show='headings')
    tipologie.heading('rimuovi', text='Rimuovi tipologia')
    tipologie.heading('id', text='')
    tipologie.heading('nome', text='Nome tipologia')
    tipologie.heading('posizione', text='')
    tipologie.heading('sfondo', text='Colore sfondo')
    tipologie.heading('visibile', text='')

    tipologie.column('rimuovi')
    tipologie.column('id')
    tipologie.column('nome')
    tipologie.column('posizione')
    tipologie.column('sfondo')
    tipologie.column('visibile')

    tipologie['displaycolumns'] = ('rimuovi', 'nome', 'sfondo')

    tipologie.pack(side='left', fill='both', expand=True)

    tipologie.bind("<Button-1>", lambda event, tip=tipologie: on_tipologie_select(event, tip))

    for item in api_get('/tipologie'):
        tipologie.insert('', 'end',
                        values=('-', item['nome'], item['sfondo'], item['id'], item['posizione'], item['visibile']))
    refresh_colori(tipologie)

    # listini_frame