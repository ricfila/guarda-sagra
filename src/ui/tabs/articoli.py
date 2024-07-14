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

def scelta_colore(intestazione, colore):
    colore_temp =colorchooser.askcolor(title = intestazione)[1]
    colore.set(colore_temp)

def on_select_colore(treeview, id_riga, nome_colonna):
    colore = tk.StringVar()
    scelta_colore(("Scelta dello sfondo per la tipologia "+ treeview.item(id_riga, 'values')[1])[1], colore)
    treeview.set(id_riga, nome_colonna, colore.get())
    # TODO chiamata a API per modifica colore
    refresh_colori(treeview)

def refresh_colori(treeview):
    for riga in treeview.get_children():
        colore = treeview.item(riga, 'values')[2]
        if colore != 'None':
            nome_tag = treeview.item(riga, 'values')[1].replace(' ', '_') + '_colore'
            treeview.tag_configure(nome_tag, background=colore)
            treeview.item(riga, tags=nome_tag)


def on_select_modifica(treeview, id_riga, indice_colonna, nome_colonna): #TODO unisci a on_select_modifica di cassa.py e sposta in modulo per funzioni generiche
    # click sinistro per modificare nome. "invio" o click fuori per modificare, "esc" per annullare
    bbox = treeview.bbox(id_riga, nome_colonna)

    if bbox:
        x, y, width, height = bbox
        valori_riga_attuali = treeview.item(id_riga, 'values')[int(indice_colonna[1:])-1]
        entry_per_modifica = ttk.Entry(treeview, width=width)
        entry_per_modifica.insert(0, valori_riga_attuali)

        def save_edit(event):
            new_value = entry_per_modifica.get()
            #TODO put_api per modifica nome
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
        #api_delete(treeview.item(id_riga, 'values')[3])  #TODO DELETE REQUEST API (api_delete è un nome temporaneo, il valore in posizione 3 è 'id')
        treeview.delete(id_riga)
def add_tipologia(tipologie_treeview, nome, posizione, colore):
    #TODO post_api(nome, posizione, colore) Devo passare altro?
    refresh_tipologie_treeview(tipologie_treeview)


def refresh_tipologie_treeview(tipologie_treeview):
    for riga in tipologie_treeview.get_children():
        tipologie_treeview.delete(riga)

    for item in api_get('/tipologie'):
        tipologie_treeview.insert('', 'end',
                        values=('-', item['nome'], item['sfondo'], item['id'], item['posizione'], item['visibile']))
    refresh_colori(tipologie_treeview)


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

    articoli_page = add_notebook_frame(articoli_notebook, 'Articoli')
    tipologie_page = add_notebook_frame(articoli_notebook, 'Tipologie')
    listini_page = add_notebook_frame(articoli_notebook, 'Listini')

    # articoli_page
    # tipologie_frame
    tipologie_view = ttk.Frame(tipologie_page)
    tipologie_view.pack(fill='both', expand=True)
    # frame di inserimento tipologie
    nuova_tipologia_frame = ttk.Frame(tipologie_view)
    nuova_tipologia_frame.pack()

    nuova_tipologia_nome_label = ttk.Label(nuova_tipologia_frame, text="Nome nuova tipologia:")
    nuova_tipologia_nome_label.pack(side='left', padx=10, pady=10)

    nuova_tipologia_nome = tk.StringVar()
    nuova_tipologia_nome_entry = ttk.Entry(nuova_tipologia_frame, textvariable=nuova_tipologia_nome)
    nuova_tipologia_nome_entry.pack(side='left', padx=10, pady=10)

    nuova_tipologia_posizione_label = ttk.Label(nuova_tipologia_frame, text="Posizione nuova tipologia:")
    nuova_tipologia_posizione_label.pack(side='left', padx=10, pady=10)

    nuova_tipologia_posizione = tk.StringVar()
    nuova_tipologia_posizione_entry = ttk.Entry(nuova_tipologia_frame, textvariable=nuova_tipologia_posizione, width=10)
    nuova_tipologia_posizione_entry.pack(side='left', padx=10, pady=10)

    nuova_tipologia_colore = tk.StringVar()
    nuova_tipologia_colore_bottone = ttk.Button(nuova_tipologia_frame, text="Seleziona colore",
                                                command = lambda : scelta_colore("Seleziona il colore di sfondo per la nuova tipologia", nuova_tipologia_colore))
    nuova_tipologia_colore_bottone.pack(side='left', padx=10, pady=10)


    tipologie_treeview = ttk.Treeview(tipologie_view, columns=('rimuovi', 'nome', 'sfondo', 'id', 'posizione', 'visibile'),
                          show='headings')
    tipologie_treeview.heading('rimuovi', text='Rimuovi tipologia')
    tipologie_treeview.heading('id', text='')
    tipologie_treeview.heading('nome', text='Nome tipologia')
    tipologie_treeview.heading('posizione', text='')
    tipologie_treeview.heading('sfondo', text='Colore sfondo')
    tipologie_treeview.heading('visibile', text='')

    tipologie_treeview.column('rimuovi')
    tipologie_treeview.column('id')
    tipologie_treeview.column('nome')
    tipologie_treeview.column('posizione')
    tipologie_treeview.column('sfondo')
    tipologie_treeview.column('visibile')

    tipologie_treeview['displaycolumns'] = ('rimuovi', 'nome', 'sfondo')

    tipologie_treeview.pack(fill='both', expand=True)

    tipologie_treeview.bind("<Button-1>", lambda event, tip=tipologie_treeview: on_tipologie_select(event, tip))

    refresh_tipologie_treeview(tipologie_treeview)

    aggiungi_tipologia = ttk.Button(nuova_tipologia_frame, text="Aggiungi tipologia", command= lambda: add_tipologia(tipologie_treeview, nuova_tipologia_nome, nuova_tipologia_posizione, nuova_tipologia_colore))
    aggiungi_tipologia.pack(side='left', padx=10, pady=10)

    # listini_page