import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from .funzioni_generiche import api_get, api_post, api_delete, crea_checkbox, on_treeview_select, refresh_treeview, scelta_colore
import functools


'''
def on_select_inverti(treeview, id_riga, indice_colonna, nome_colonna):
    pass
    #if valore 0 == +
    #    aggiungi associazione a db, colora di verde, scrivi -
    #if valore 0 == -
    #    rimuovi da db, setta colore base, scrivi +
'''
def add_to_treeview(treeview, nome_treeview, valori):
    data_to_send = {}
    if nome_treeview != 'listini_treeview':
        for item in valori:
            data_to_send[item[0]] = item[1]
    else:
        data_to_send[valori[0]] = valori[1]

    response = api_post('/' + (nome_treeview.split('_'))[0], data_to_send)

    if response == 201:
        pass
    refresh_treeview(treeview, nome_treeview, '/'+(nome_treeview.split('_'))[0])


def add_tipologia(tipologie_treeview, valori_tipologia):  #TODO parametrizza con (nome_treeview.split('_'))[0]
    data_to_send = {}
    for item in valori_tipologia:
        data_to_send[item[0]] = item[1]

    response = api_post('/tipologie', data_to_send)

    if response == 201:
        pass
    refresh_treeview(tipologie_treeview, 'tipologie_treeview', '/tipologie')

'''
def get_tipologie(combobox):  #TODO parametrizza con (nome_treeview.split('_'))[0]
    tipologie = []
    for item in api_get('/tipologie'):
        tipologia = str(item['id']) + ' ' + item['nome']
        tipologie.append(tipologia)
    combobox['values'] = tuple(tipologie)

def get_listini(combobox):  #TODO parametrizza con (nome_treeview.split('_'))[0]
    listini = []
    for item in api_get('/listini'):
        listino = str(item['id']) + ' ' + item['nome']
        listini.append(listino)
    combobox['values'] = tuple(listini)

def get_profili(combobox):  #TODO parametrizza con (nome_treeview.split('_'))[0]
    profili = []
    for item in api_get('/profili'):
        profilo = str(item['id']) + ' ' + item['nome']
        profili.append(profilo)
    combobox['values'] = tuple(profili)
'''
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
    #articoli_listini_page = add_notebook_frame(articoli_notebook, 'Collega articoli a listini')

    # articoli_page

    articoli_view = ttk.Frame(articoli_page)
    articoli_view.pack(fill='both', expand=True)
    # frame di inserimento articoli
    nuovo_articolo_frame = ttk.Frame(articoli_view)
    nuovo_articolo_frame.pack(side='top')

    fields_nuovo_articolo_frame = ttk.Frame(nuovo_articolo_frame)
    fields_nuovo_articolo_frame.pack(side='left')
    checkboxes_nuovo_articolo_frame = ttk.Frame(nuovo_articolo_frame)
    checkboxes_nuovo_articolo_frame.pack(side='left')

    n_fields_nuovo_articolo_frame = ttk.Frame(fields_nuovo_articolo_frame)
    n_fields_nuovo_articolo_frame.pack(side='top')
    s_fields_nuovo_articolo_frame = ttk.Frame(fields_nuovo_articolo_frame)
    s_fields_nuovo_articolo_frame.pack(side='top')
    n_checkboxes_nuovo_articolo_frame = ttk.Frame(checkboxes_nuovo_articolo_frame)
    n_checkboxes_nuovo_articolo_frame.pack(side='top')
    s_checkboxes_nuovo_articolo_frame = ttk.Frame(checkboxes_nuovo_articolo_frame)
    s_checkboxes_nuovo_articolo_frame.pack(side='top')


    nuovo_articolo_nome_label = ttk.Label(n_fields_nuovo_articolo_frame, text="Nome nuovo articolo:")
    nuovo_articolo_nome_label.pack(side='left', padx=10, pady=10)

    nuovo_articolo_nome = tk.StringVar()
    nuovo_articolo_nome_entry = ttk.Entry(n_fields_nuovo_articolo_frame, textvariable=nuovo_articolo_nome)
    nuovo_articolo_nome_entry.pack(side='left', padx=10, pady=10)

    nuovo_articolo_nome_breve_label = ttk.Label(s_fields_nuovo_articolo_frame, text="Nome breve nuovo articolo:")
    nuovo_articolo_nome_breve_label.pack(side='left', padx=10, pady=10)

    nuovo_articolo_nome_breve = tk.StringVar()
    nuovo_articolo_nome_breve_entry = ttk.Entry(s_fields_nuovo_articolo_frame, textvariable=nuovo_articolo_nome_breve)
    nuovo_articolo_nome_breve_entry.pack(side='left', padx=10, pady=10)

    #TODO ESEMPIO DI COMBOBOX PER TIPOLOGIE
    '''
    nuovo_articolo_tipologia = tk.StringVar()
    nuovo_articolo_tipologia_combobox = ttk.Combobox(nuovo_articolo_frame, textvariable=nuovo_articolo_tipologia)
    nuovo_articolo_tipologia_combobox['state'] = 'readonly'
    nuovo_articolo_tipologia_combobox.pack(side='left', padx=10, pady=10)

    aggiorna_combobox_listino = ttk.Button(nuovo_articolo_frame, text="Aggiorna listino",
                                           command=lambda: get_tipologie(nuovo_articolo_tipologia_combobox))
    aggiorna_combobox_listino.pack(side='left', padx=10, pady=10)
    '''

    nuovo_articolo_prezzo_label = ttk.Label(n_fields_nuovo_articolo_frame, text="Prezzo:")
    nuovo_articolo_prezzo_label.pack(side='left', padx=10, pady=10)

    nuovo_articolo_prezzo = tk.StringVar()
    nuovo_articolo_prezzo_entry = ttk.Entry(n_fields_nuovo_articolo_frame, textvariable=nuovo_articolo_prezzo, width=10)
    nuovo_articolo_prezzo_entry.pack(side='left', padx=10, pady=10)


    copia_cliente = tk.BooleanVar()
    copia_cucina = tk.BooleanVar()
    copia_bar = tk.BooleanVar()
    copia_pizzeria = tk.BooleanVar()
    copia_rosticceria = tk.BooleanVar()

    copia_cliente_checkbox = crea_checkbox(n_checkboxes_nuovo_articolo_frame, "Copia cliente", copia_cliente)
    copia_cucina_checkbox = crea_checkbox(s_checkboxes_nuovo_articolo_frame, "Copia cucina", copia_cucina)
    copia_bar_checkbox = crea_checkbox(n_checkboxes_nuovo_articolo_frame, "Copia bar", copia_bar)
    copia_pizzeria_checkbox = crea_checkbox(s_checkboxes_nuovo_articolo_frame, "Copia pizzeria", copia_pizzeria)
    copia_rosticceria_checkbox = crea_checkbox(n_checkboxes_nuovo_articolo_frame, "Copia rosticceria", copia_rosticceria)
    copia_cliente_checkbox.pack(side='left', padx=5, pady=5)
    copia_cucina_checkbox.pack(side='left', padx=5, pady=5)
    copia_bar_checkbox.pack(side='left', padx=5, pady=5)
    copia_pizzeria_checkbox.pack(side='left', padx=5, pady=5)
    copia_rosticceria_checkbox.pack(side='left', padx=5, pady=5)

    def prepara_salvataggio(articoli_treeview):
        valori_articolo = (
            ('nome', str(nuovo_articolo_nome.get())),
            ('nome_breve', str(nuovo_articolo_nome_breve.get())),
            ('prezzo', str(nuovo_articolo_prezzo.get())),
            ('copia_cliente', copia_cliente.get()),
            ('copia_cucina', copia_cucina.get()),
            ('copia_bar', copia_bar.get()),
            ('copia_pizzeria', copia_pizzeria.get()),
            ('copia_rosticceria', copia_rosticceria.get())
        )
        add_to_treeview(articoli_treeview, 'articoli_treeview', valori_articolo)

    def pulisci_campi():
        nuovo_articolo_nome.set('')
        nuovo_articolo_nome_breve.set('')
        nuovo_articolo_prezzo.set('')
        copia_cliente.set(False)
        copia_cucina.set(False)
        copia_bar.set(False)
        copia_pizzeria.set(False)
        copia_rosticceria.set(False)


    aggiungi_articolo_pulsante = ttk.Button(nuovo_articolo_frame, text="Aggiungi articolo", command=lambda: prepara_salvataggio(articoli_treeview))
    aggiungi_articolo_pulsante.pack(side='left', padx=10, pady=10)

    pulisci_campi_pulsante = ttk.Button(nuovo_articolo_frame, text="Pulisci campi", command=lambda: pulisci_campi())
    pulisci_campi_pulsante.pack(side='left', padx=(100, 10), pady=10)

    aggiorna_articoli_pulsante = ttk.Button(nuovo_articolo_frame, text="Aggiorna articoli", command=lambda: refresh_treeview(articoli_treeview, 'articoli_treeview', '/articoli'))
    aggiorna_articoli_pulsante.pack(side='left', padx=10, pady=10)


    articoli_treeview = ttk.Treeview(articoli_view, columns=('rimuovi', 'id', 'nome', 'nome_breve', 'prezzo', 'copia_cliente', 'copia_cucina', 'copia_bar', 'copia_pizzeria', 'copia_rosticceria'),
                          show='headings')
    articoli_treeview.heading('rimuovi', text='Rimuovi articolo')
    articoli_treeview.heading('id', text='Id articolo')
    articoli_treeview.heading('nome', text='Nome articolo')
    articoli_treeview.heading('nome_breve', text='Nome breve articolo')
    articoli_treeview.heading('prezzo', text='Prezzo')
    articoli_treeview.heading('copia_cliente', text='Copia Cliente')
    articoli_treeview.heading('copia_cucina', text='Copia cucina')
    articoli_treeview.heading('copia_bar', text='Copia bar')
    articoli_treeview.heading('copia_pizzeria', text='Copia pizzeria')
    articoli_treeview.heading('copia_rosticceria', text='Copia rosticceria')

    articoli_treeview.column('rimuovi', width=40)
    articoli_treeview.column('copia_cliente', width=40)
    articoli_treeview.column('copia_cucina', width=40)
    articoli_treeview.column('copia_bar', width=40)
    articoli_treeview.column('copia_pizzeria', width=40)
    articoli_treeview.column('copia_rosticceria', width=40)

    articoli_treeview.pack(fill='both', expand=True)

    articoli_treeview.bind("<ButtonRelease-1>", lambda event, tip=articoli_treeview: on_treeview_select(event, 'articoli_treeview', tip))

    refresh_treeview(articoli_treeview, 'articoli_treeview', '/articoli')

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

    visibile = tk.BooleanVar()
    visibile_checkbox = crea_checkbox(nuova_tipologia_frame, "Visibile", visibile)
    visibile_checkbox.pack(side='left', padx=5, pady=5)

    tipologie_treeview = ttk.Treeview(tipologie_view, columns=('rimuovi', 'id', 'nome', 'posizione', 'sfondo', 'visibile'),
                          show='headings')
    tipologie_treeview.heading('rimuovi', text='Rimuovi tipologia')
    tipologie_treeview.heading('id', text='Id')
    tipologie_treeview.heading('nome', text='Nome tipologia')
    tipologie_treeview.heading('posizione', text='Posizione')
    tipologie_treeview.heading('sfondo', text='Colore sfondo')
    tipologie_treeview.heading('visibile', text='Visibile')

    tipologie_treeview.column('rimuovi', width=40)

    tipologie_treeview.pack(fill='both', expand=True)

    tipologie_treeview.bind("<ButtonRelease-1>", lambda event, tip=tipologie_treeview: on_treeview_select(event, 'tipologie_treeview', tip))

    refresh_treeview(tipologie_treeview, 'tipologie_treeview','/tipologie')

    def prepara_salvataggio_tipologia(tipologie_treeview):
        valori_tipologia = (
            ('nome', str(nuova_tipologia_nome.get())),
            ('posizione', str(nuova_tipologia_posizione.get())),
            ('sfondo', str(nuova_tipologia_colore.get())),
            ('visibile', visibile.get())
        )
        add_to_treeview(tipologie_treeview, 'tipologie_treeview', valori_tipologia)

    aggiungi_tipologia = ttk.Button(nuova_tipologia_frame, text="Aggiungi tipologia", command= lambda: prepara_salvataggio_tipologia(tipologie_treeview))
    aggiungi_tipologia.pack(side='left', padx=10, pady=10)

    def pulisci_campi_tipologia():
        nuova_tipologia_nome.set('')
        nuova_tipologia_posizione.set('')
        nuova_tipologia_colore.set('')
    pulisci_campi_tipologia_pulsante = ttk.Button(nuova_tipologia_frame, text="Pulisci campi", command= lambda: pulisci_campi_tipologia())
    pulisci_campi_tipologia_pulsante.pack(side='left', padx=(100, 10), pady=10)

    aggiorna_tipologia_pulsante = ttk.Button(nuova_tipologia_frame, text="Aggiorna tipologie", command=lambda: refresh_treeview(tipologie_treeview, 'tipologie_treeview', '/tipologie'))
    aggiorna_tipologia_pulsante.pack(side='left', padx=10, pady=10)



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

    aggiungi_listino = ttk.Button(nuovo_listino_frame, text="Aggiungi listino", command= lambda: add_to_treeview(listini_treeview, 'listini_treeview', (('nome', nuovo_listino_nome.get()))))
    aggiungi_listino.pack(side='left', padx=10, pady=10)

    listini_treeview = ttk.Treeview(listini_view, columns=('rimuovi', 'id', 'nome'),
                          show='headings')

    listini_treeview.heading('rimuovi', text='Rimuovi listino')
    listini_treeview.heading('id', text='Id listino')
    listini_treeview.heading('nome', text='Nome listino')

    listini_treeview.column('rimuovi', width=40)
    listini_treeview.pack(fill='both', expand=True)

    listini_treeview.bind("<ButtonRelease-1>", lambda event, lis=listini_treeview: on_treeview_select(event, 'listini_treeview', lis))

    refresh_treeview(listini_treeview, 'listini_treeview','/listini')

    aggiorna_listini_pulsante = ttk.Button(nuovo_listino_frame, text="Aggiorna listini", command=lambda: refresh_treeview(listini_treeview, 'listini_treeview', '/listini'))
    aggiorna_listini_pulsante.pack(side='left', padx=(100,10), pady=10)


    #TODO articoli_listini
    '''
    # articoli_listini_page

    articoli_listini_view = ttk.Frame(articoli_listini_page)
    articoli_listini_view.pack(fill='both', expand=True)

    scegli_listino_frame = ttk.Frame(articoli_listini_view)
    scegli_listino_frame.pack(side='top')

    modifica_listino_label = ttk.Label(scegli_listino_frame, text="Listino da modificare:")
    modifica_listino_label.pack(side='left', padx=10, pady=10)

    modifica_listino_id_nome = tk.StringVar()
    modifica_listino_id_nome_combobox = ttk.Combobox(scegli_listino_frame, textvariable=modifica_listino_id_nome)
    modifica_listino_id_nome_combobox['state'] = 'readonly'
    modifica_listino_id_nome_combobox.pack(side='left', padx=10, pady=10)
    get_listini(modifica_listino_id_nome_combobox)

    aggiorna_combobox_listino = ttk.Button(scegli_listino_frame, text="Aggiorna elenco listini", command= lambda: get_listini(modifica_listino_id_nome_combobox))
    aggiorna_combobox_listino.pack(side='left', padx=10, pady=10)

    # TODO da mettere in tab profili/ sottotab listini
    
    cassa_per_listino = tk.StringVar()
    collega_cassa_a_listino_combobox = ttk.Combobox(scegli_listino_frame, textvariable=cassa_per_listino)
    collega_cassa_a_listino_combobox['state'] = 'readonly'
    collega_cassa_a_listino_combobox.pack(side='left', padx=10, pady=10)

    aggiorna_combobox_cassa_listino = ttk.Button(scegli_listino_frame, text="Aggiorna casse",
                                           command=lambda: get_profili(collega_cassa_a_listino_combobox))
    aggiorna_combobox_cassa_listino.pack(side='left', padx=10, pady=10)
    # TODO FINE da mettere in tab profili/ sottotab listini

    articoli_per_listino_treeview = ttk.Treeview(articoli_listini_view, columns=('aggiungi_rimuovi', 'id', 'nome', 'nome_breve', 'prezzo', 'sfondo', 'tipologia', 'nome_tipologia', 'sfondo_tipologia'),
                          show='headings')

    articoli_per_listino_treeview.heading('aggiungi_rimuovi', text='Aggiungi/rimuovi articolo')
    articoli_per_listino_treeview.heading('id', text='Id articolo')
    articoli_per_listino_treeview.heading('nome', text='Nome articolo')
    articoli_per_listino_treeview.heading('nome_breve', text='Nome breve articolo')
    articoli_per_listino_treeview.heading('prezzo', text='Prezzo')
    articoli_per_listino_treeview.heading('sfondo', text='Sfondo articolo')
    articoli_per_listino_treeview.heading('tipologia', text='Id tipologia')
    articoli_per_listino_treeview.heading('nome_tipologia', text='Nome tipologia')
    articoli_per_listino_treeview.heading('sfondo_tipologia', text='Sfondo tipologia')

    articoli_per_listino_treeview.column('aggiungi_rimuovi', width=40)

    modifica_listino_id_nome_combobox.bind("<<ComboboxSelected>>", lambda event, apl=articoli_per_listino_treeview: refresh_treeview(apl, 'articoli_per_listino_treeview', '/articoli', '/articoli_listino/' + (modifica_listino_id_nome.get()[0]), '/articoli_listino_tipologie/' + (modifica_listino_id_nome.get()[0])))

    articoli_per_listino_treeview.pack(fill='both', expand=True)

    articoli_per_listino_treeview.bind("<ButtonRelease-1>", lambda event, apl=articoli_per_listino_treeview: on_treeview_select(event, 'articoli_per_listino', apl))
    '''