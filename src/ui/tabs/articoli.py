import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, colorchooser
import requests
import json
from config import api_get, api_post


def toggle_checkbox(event, var):  # TODO sposta in file funzioni generiche unisci con cassa
    var.set(not var.get())


def crea_checkbox(parent_frame, label_text, var):  # TODO sposta in file funzioni generiche unisci con cassa
    frame = tk.Frame(parent_frame, borderwidth=1, relief=tk.RIDGE)

    checkbox = tk.Checkbutton(frame, variable=var, onvalue=True, offvalue=False)
    checkbox.pack(side='left')

    label = tk.Label(frame, text=label_text)
    label.pack(side='left', padx=5)

    frame.bind("<ButtonRelease-1>", lambda event: toggle_checkbox(event, var))
    label.bind("<ButtonRelease-1>", lambda event: toggle_checkbox(event, var))

    return frame

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

def on_articoli_select(event, treeview): #TODO unisci a on_select di cassa.py e sposta in modulo per funzioni generiche
    region = treeview.identify("region", event.x, event.y)
    if region == "cell":
        indice_colonna = treeview.identify_column(event.x)
        nome_colonna = treeview.column(indice_colonna)['id']
        id_riga = treeview.identify_row(event.y)
        if nome_colonna == 'nome':
            on_select_modifica(treeview, id_riga, indice_colonna, nome_colonna)

        elif nome_colonna == 'rimuovi':
            on_select_rimuovi(treeview, id_riga)

def on_articoli_per_listino_select(event, treeview):
    region = treeview.identify("region", event.x, event.y)
    if region == "cell":
        indice_colonna = treeview.identify_column(event.x)
        nome_colonna = treeview.column(indice_colonna)['id']
        id_riga = treeview.identify_row(event.y)
        if nome_colonna == 'aggiungi_rimuovi':
            on_select_inverti(treeview, id_riga, indice_colonna, nome_colonna)


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

def on_select_inverti(treeview, id_riga, indice_colonna, nome_colonna):
    pass
    #if valore 0 == +
    #    aggiungi associazione a db, colora di verde, scrivi -
    #if valore 0 == -
    #    rimuovi da db, setta colore base, scrivi +

def on_select_rimuovi(treeview, id_riga):
    reply = messagebox.askquestion("Elimina tipologia", f"Vuoi eliminare la tipologia " + treeview.item(id_riga, 'values')[1])
    if reply == 'yes':
        #api_delete(treeview.item(id_riga, 'values')[3])  #TODO DELETE REQUEST API (api_delete è un nome temporaneo, il valore in posizione 3 è 'id')
        treeview.delete(id_riga)
def add_articolo(articoli_treeview, nome, nome_breve, id_tipologia, prezzo, copia_cliente, copia_cucina, copia_bar, copia_pizzeria, copia_rosticceria):
    #TODO post_api(nome, nome_breve, ...) Devo passare altro?
    refresh_articoli_treeview(articoli_treeview)


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

def refresh_articoli_treeview(articoli_treeview):
    for riga in articoli_treeview.get_children():
        articoli_treeview.delete(riga)

    for item in api_get('/articoli'):  #TODO manca API per get di articoli senza id listino
        articoli_treeview.insert('', 'end',
                        values=('-', item['id'],  item['nome'], item['nome_breve'], item['tipologia'], item['prezzo'], item['copia_cliente'], item['copia_cucina'], item['copia_bar'], item['copia_pizzeria'], item['copia_rosticceria']))

def get_tipologie(combobox):
    tipologie = []
    for item in api_get('/tipologie'):
        tipologia = str(item['id']) + ' ' + item['nome']
        tipologie.append(tipologia)
    combobox['values'] = tuple(tipologie)

def get_listini(combobox):
    listini = []
    for item in api_get('/listini'):
        listino = str(item['id']) + ' ' + item['nome']
        listini.append(listino)
    combobox['values'] = tuple(listini)

def get_profili(combobox):
    profili = []
    for item in api_get('/profili'):
        profilo = str(item['id']) + ' ' + item['nome']
        profili.append(profilo)
    combobox['values'] = tuple(profili)

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

    articoli_view = ttk.Frame(articoli_page)
    articoli_view.pack(fill='both', expand=True)
    # frame di inserimento articoli
    nuovo_articolo_frame = ttk.Frame(articoli_view)
    nuovo_articolo_frame.pack()

    nuovo_articolo_nome_label = ttk.Label(nuovo_articolo_frame, text="Nome nuovo articolo:")
    nuovo_articolo_nome_label.pack(side='left', padx=10, pady=10)

    nuovo_articolo_nome = tk.StringVar()
    nuovo_articolo_nome_entry = ttk.Entry(nuovo_articolo_frame, textvariable=nuovo_articolo_nome)
    nuovo_articolo_nome_entry.pack(side='left', padx=10, pady=10)

    nuovo_articolo_nome_breve_label = ttk.Label(nuovo_articolo_frame, text="Nome breve nuovo articolo:")
    nuovo_articolo_nome_breve_label.pack(side='left', padx=10, pady=10)

    nuovo_articolo_nome_breve = tk.StringVar()
    nuovo_articolo_nome_breve_entry = ttk.Entry(nuovo_articolo_frame, textvariable=nuovo_articolo_nome_breve)
    nuovo_articolo_nome_breve_entry.pack(side='left', padx=10, pady=10)

    nuovo_articolo_tipologia = tk.StringVar()
    nuovo_articolo_tipologia_combobox = ttk.Combobox(nuovo_articolo_frame, textvariable=nuovo_articolo_tipologia)
    nuovo_articolo_tipologia_combobox['state'] = 'readonly'
    nuovo_articolo_tipologia_combobox.pack(side='left', padx=10, pady=10)

    aggiorna_combobox_listino = ttk.Button(nuovo_articolo_frame, text="Aggiorna listino",
                                           command=lambda: get_tipologie(nuovo_articolo_tipologia_combobox))
    aggiorna_combobox_listino.pack(side='left', padx=10, pady=10)


    nuovo_articolo_prezzo_label = ttk.Label(nuovo_articolo_frame, text="Prezzo:")
    nuovo_articolo_prezzo_label.pack(side='left', padx=10, pady=10)

    nuovo_articolo_prezzo = tk.StringVar()
    nuovo_articolo_prezzo_entry = ttk.Entry(nuovo_articolo_frame, textvariable=nuovo_articolo_prezzo, width=10)
    nuovo_articolo_prezzo_entry.pack(side='left', padx=10, pady=10)


    copia_cliente = tk.BooleanVar()
    copia_cucina = tk.BooleanVar()
    copia_bar = tk.BooleanVar()
    copia_pizzeria = tk.BooleanVar()
    copia_rosticceria = tk.BooleanVar()

    copia_cliente_checkbox = crea_checkbox(nuovo_articolo_frame, "Copia cliente", copia_cliente)
    copia_cucina_checkbox = crea_checkbox(nuovo_articolo_frame, "Copia cucina", copia_cucina)
    copia_bar_checkbox = crea_checkbox(nuovo_articolo_frame, "Copia bar", copia_bar)
    copia_pizzeria_checkbox = crea_checkbox(nuovo_articolo_frame, "Copia pizzeria", copia_pizzeria)
    copia_rosticceria = crea_checkbox(nuovo_articolo_frame, "Copia rosticceria", copia_rosticceria)
    copia_cliente_checkbox.pack(side='left', padx=5, pady=5)
    copia_cucina_checkbox.pack(side='left', padx=5, pady=5)
    copia_bar_checkbox.pack(side='left', padx=5, pady=5)
    copia_pizzeria_checkbox.pack(side='left', padx=5, pady=5)
    copia_rosticceria.pack(side='left', padx=5, pady=5)


    articoli_treeview = ttk.Treeview(articoli_view, columns=('rimuovi', 'id', 'nome', 'nome_breve', 'tipologia', 'prezzo', 'copia_cliente', 'copia_cucina', 'copia_bar', 'copia_pizzeria', 'copia_rosticceria'),
                          show='headings')
    articoli_treeview.heading('rimuovi', text='Rimuovi articolo')
    articoli_treeview.heading('id', text='Id articolo')
    articoli_treeview.heading('nome', text='Nome articolo')
    articoli_treeview.heading('nome_breve', text='Nome breve articolo')
    articoli_treeview.heading('tipologia', text='Tipologia articolo')
    articoli_treeview.heading('prezzo', text='Prezzo')
    articoli_treeview.heading('copia_cliente', text='Copia Cliente')
    articoli_treeview.heading('copia_cucina', text='Copia cucina')
    articoli_treeview.heading('copia_bar', text='Copia bar')
    articoli_treeview.heading('copia_pizzeria', text='Copia pizzeria')
    articoli_treeview.heading('copia_rosticceria', text='Copia rosticceria')

    articoli_treeview.column('rimuovi', width=40)
    articoli_treeview.column('id')
    articoli_treeview.column('nome')
    articoli_treeview.column('nome_breve')
    articoli_treeview.column('tipologia')
    articoli_treeview.column('prezzo')
    articoli_treeview.column('copia_cliente', width=40)
    articoli_treeview.column('copia_cucina', width=40)
    articoli_treeview.column('copia_bar', width=40)
    articoli_treeview.column('copia_pizzeria', width=40)
    articoli_treeview.column('copia_rosticceria', width=40)

    #articoli_treeview['displaycolumns'] = ('rimuovi', 'nome', 'tipologia')

    articoli_treeview.pack(fill='both', expand=True)

    articoli_treeview.bind("<ButtonRelease-1>", lambda event, tip=articoli_treeview: on_articoli_select(event, tip))

    #refresh_articoli_treeview(articoli_treeview)

    #aggiungi_articolo = ttk.Button(nuovo_articolo_frame, text="Aggiungi articolo", command= lambda: add_articolo(articoli_treeview, nuovo_articolo_nome.get(), nuovo_articolo_nome_breve.get(), nuovo_articolo_tipologia.get()[0], nuovo_articolo_prezzo.get(), copia_cliente.get(), copia_cucina.get(), copia_bar.get(), copia_pizzeria.get(), copia_rosticceria.get()))
    #aggiungi_articolo.pack(side='left', padx=10, pady=10)


    # tipologie_page
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

    tipologie_treeview.column('rimuovi', width=40)
    tipologie_treeview.column('id')
    tipologie_treeview.column('nome')
    tipologie_treeview.column('posizione')
    tipologie_treeview.column('sfondo')
    tipologie_treeview.column('visibile')

    tipologie_treeview['displaycolumns'] = ('rimuovi', 'nome', 'sfondo')

    tipologie_treeview.pack(fill='both', expand=True)

    tipologie_treeview.bind("<ButtonRelease-1>", lambda event, tip=tipologie_treeview: on_tipologie_select(event, tip))

    refresh_tipologie_treeview(tipologie_treeview)

    aggiungi_tipologia = ttk.Button(nuova_tipologia_frame, text="Aggiungi tipologia", command= lambda: add_tipologia(tipologie_treeview, nuova_tipologia_nome, nuova_tipologia_posizione, nuova_tipologia_colore))
    aggiungi_tipologia.pack(side='left', padx=10, pady=10)

    # listini_page

    listini_view = ttk.Frame(listini_page)
    listini_view.pack(fill='both', expand=True)
    # frame di inserimento articoli
    nuovo_listino_frame = ttk.Frame(listini_view)
    nuovo_listino_frame.pack()

    nuovo_listino_nome_label = ttk.Label(nuovo_listino_frame, text="Nome nuovo listino:")
    nuovo_listino_nome_label.pack(side='left', padx=10, pady=10)

    nuovo_listino_nome = tk.StringVar()
    nuovo_listino_nome_entry = ttk.Entry(nuovo_listino_frame, textvariable=nuovo_listino_nome)
    nuovo_listino_nome_entry.pack(side='left', padx=10, pady=10)

    #aggiungi_listino = ttk.Button(nuovo_listino_frame, text="Aggiungi listino", command= lambda: add_listino(tipologie_treeview, nuova_tipologia_nome, nuova_tipologia_posizione, nuova_tipologia_colore))
    #aggiungi_listino.pack(side='left', padx=10, pady=10)

    modifica_listino_frame = ttk.Frame(listini_view)
    modifica_listino_frame.pack()

    modifica_listino_label = ttk.Label(modifica_listino_frame, text="Listino da modificare:")
    modifica_listino_label.pack(side='left', padx=10, pady=10)

    modifica_listino_id_nome = tk.StringVar()
    modifica_listino_id_nome_combobox = ttk.Combobox(modifica_listino_frame, textvariable=modifica_listino_id_nome)
    modifica_listino_id_nome_combobox['state'] = 'readonly'
    modifica_listino_id_nome_combobox.pack(side='left', padx=10, pady=10)

    aggiorna_combobox_listino = ttk.Button(modifica_listino_frame, text="Aggiorna listino", command= lambda: get_listini(modifica_listino_id_nome_combobox))
    aggiorna_combobox_listino.pack(side='left', padx=10, pady=10)

    cassa_per_listino = tk.StringVar()
    collega_cassa_a_listino_combobox = ttk.Combobox(modifica_listino_frame, textvariable=cassa_per_listino)
    collega_cassa_a_listino_combobox['state'] = 'readonly'
    collega_cassa_a_listino_combobox.pack(side='left', padx=10, pady=10)

    aggiorna_combobox_cassa_listino = ttk.Button(modifica_listino_frame, text="Aggiorna casse",
                                           command=lambda: get_profili(collega_cassa_a_listino_combobox))
    aggiorna_combobox_cassa_listino.pack(side='left', padx=10, pady=10)


    articoli_per_listino_treeview = ttk.Treeview(listini_view, columns=('aggiungi_rimuovi', 'id', 'nome', 'nome_breve', 'tipologia', 'prezzo'),
                          show='headings')

    articoli_per_listino_treeview.heading('aggiungi_rimuovi', text='Aggiungi/rimuovi articolo')
    articoli_per_listino_treeview.heading('id', text='Id articolo')
    articoli_per_listino_treeview.heading('nome', text='Nome articolo')
    articoli_per_listino_treeview.heading('nome_breve', text='Nome breve articolo')
    articoli_per_listino_treeview.heading('tipologia', text='Id tipologia')
    articoli_per_listino_treeview.heading('prezzo', text='Prezzo')

    articoli_per_listino_treeview.column('aggiungi_rimuovi', width=40)
    articoli_per_listino_treeview.column('id')
    articoli_per_listino_treeview.column('nome')
    articoli_per_listino_treeview.column('nome_breve')
    articoli_per_listino_treeview.column('tipologia')
    articoli_per_listino_treeview.column('prezzo')

    #articoli_per_listino_treeview['displaycolumns'] = ('rimuovi', 'nome', 'sfondo')

    articoli_per_listino_treeview.pack(fill='both', expand=True)

    articoli_per_listino_treeview.bind("<ButtonRelease-1>", lambda event, apl=articoli_per_listino_treeview: on_articoli_per_listino_select(event, apl))

    #refresh_?? (articoli_per_listino_treeview)