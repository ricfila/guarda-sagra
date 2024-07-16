import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import functools
from .funzioni_generiche import api_get, api_post, crea_checkbox, on_treeview_select, update_bill

def salva(ordini_treeview, valori_ordine, bill, bill_formatted_text): #TODO Bisognerebbe anche mettere in sicurezza sta roba, ovvero oltre ai dati che invia normalmente la cassa dovrebbe inviare ad esempio una stringa identificativa della sessione che ha ricevuto dal server al momento del login. Facciamo che ci penseremo più avanti
    data_to_send = {}

    for item in valori_ordine:
        data_to_send[item[0]] = item[1]

    articles = []
    for item in ordini_treeview.get_children():
        item_data = {}
        for column in ('qta', 'note', 'id_listino', 'id_articolo'):
            item_data[column] = ordini_treeview.item(item, 'values')[ordini_treeview['columns'].index(column)]
        articles.append(item_data)

    data_to_send['articoli'] = articles

    response = api_post('/ordini', data_to_send)

    if response == 201:
        for item in ordini_treeview.get_children():
            ordini_treeview.delete(item)
        update_bill(ordini_treeview, bill, bill_formatted_text)

def max_4_chars_and_only_digits(string):
    return string.isdigit() and max_4_chars(string)

def max_4_chars(text):
    return len(text) <= 4

def insert_order(ordini_treeview, articolo, id_listino, bill, bill_formatted_text):
    matching_item = next((item for item in ordini_treeview.get_children() if ordini_treeview.item(item)['values'][6] == articolo['id']), None)

    if matching_item:
        current_values = ordini_treeview.item(matching_item)['values']
        new_first_value = int(current_values[1]) + 1
        updated_values = ('-', str(new_first_value),) + tuple(current_values[2:])
        ordini_treeview.item(matching_item, values=updated_values)
    else:
        ordini_treeview.insert('', 'end', values=('-','1', articolo['nome_breve'], articolo['prezzo'], '', id_listino, articolo['id']))
    update_bill(ordini_treeview, bill, bill_formatted_text)

def draw_cassa(notebook, profile):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Cassa")

    # inizializzo variabili usate in bill_frame
    bill = tk.DoubleVar()
    bill_formatted_text = tk.StringVar()

    # suddivido in frames:
    info_frame = ttk.Frame(tab)
    bill_frame = ttk.Frame(tab)
    options_frame = ttk.Frame(tab)

    # configuro la griglia
    tab.columnconfigure((0, 1), weight=1, uniform='a')
    tab.rowconfigure(0, weight=1, uniform='a')
    tab.rowconfigure(1, weight=6, uniform='a')
    tab.rowconfigure(2, weight=2, uniform='a')

    # posiziono i frame
    info_frame.grid(row=0, column=0, sticky='nswe')
    bill_frame.grid(row=2, column=0, sticky='nsew')
    options_frame.grid(row=0, column=1, sticky='nsew')

    # gestisco treeview per ordini

    ordini_treeview = ttk.Treeview(tab,
                          columns=('rimuovi', 'qta', 'piatto', 'prezzo', 'note', 'id_listino', 'id_articolo'),
                          show='headings')

    ordini_treeview['displaycolumns'] = ('rimuovi', 'qta', 'piatto', 'prezzo', 'note')

    ordini_treeview.heading('rimuovi', text='Rimuovi')
    ordini_treeview.heading('qta', text='Qtà')
    ordini_treeview.heading('piatto', text='Piatto')
    ordini_treeview.heading('prezzo', text='Prezzo')
    ordini_treeview.heading('note', text='Note')
    ordini_treeview.heading('id_listino', text='Id listino')
    ordini_treeview.heading('id_articolo', text='Id articolo')

    ordini_treeview.grid(row=1, column=0, sticky='nswe')
    ordini_treeview.bind("<ButtonRelease-1>", lambda event, ord=ordini_treeview: on_treeview_select(event,
                                                                                                    'ordini_treeview',
                                                                                                    ord, bill, bill_formatted_text))

    ordini_treeview.column('rimuovi', width=40)
    #click sinistro su nota per modificare. "invio" per modificare, "esc" per annullare. click sinistro su rimuovi per rimuovere

    # suddivido e gestisco info_frame
    n_info_frame = ttk.Frame(info_frame)
    n_info_frame.pack(side='top', expand=True, fill='both')
    s_info_frame = ttk.Frame(info_frame)
    s_info_frame.pack(side='top', expand=True, fill='both')

    cliente_label = ttk.Label(n_info_frame, text="Cliente:")
    cliente_name = tk.StringVar()
    cliente_name_entry = ttk.Entry(n_info_frame, textvariable=cliente_name, width=100)
    cliente_label.pack(side='left', padx=(10, 2))
    cliente_name_entry.pack(side='left', padx=(2, 10))

    coperti_label = ttk.Label(n_info_frame, text="Coperti:")
    coperti_name = tk.StringVar()
    coperti_name_entry = ttk.Entry(n_info_frame, textvariable=coperti_name, validate='key',
                                   validatecommand=(n_info_frame.register(max_4_chars_and_only_digits), '%P'), width=4)  #TODO validate fa verifica su input. da rivedere, usa come esempio
    coperti_label.pack(side='left', padx=(10, 2))
    coperti_name_entry.pack(side='left', padx=(2, 10))

    tavolo_label = ttk.Label(n_info_frame, text="Tavolo:")
    tavolo_name = tk.StringVar()
    tavolo_name_entry = ttk.Entry(n_info_frame, textvariable=tavolo_name, validate='key',
                                  validatecommand=(n_info_frame.register(max_4_chars), '%P'), width=4)  #TODO validate fa verifica su input. da rivedere, usa come esempio
    tavolo_label.pack(side='left', padx=(10, 2))
    tavolo_name_entry.pack(side='left', padx=(2, 10))

    note_ordine_label = ttk.Label(s_info_frame, text="Note:")
    note_ordine_name = tk.StringVar()
    note_ordine_name_entry = ttk.Entry(s_info_frame, textvariable=note_ordine_name)
    note_ordine_label.pack(side='left', padx=(10, 2))
    note_ordine_name_entry.pack(side='left', padx=(2, 20), expand=True, fill='x')

    # gestisco notebook per la scelta articoli
    lista_listini = api_get('/listini_cassa/', id_profilo=profile['id'])

    listini_notebook = ttk.Notebook(tab)
    listini_notebook.grid(row=1, column=1, rowspan=2, sticky='nsew')

    for item_listino in lista_listini:
        listino = ttk.Frame(listini_notebook)
        listini_notebook.add(listino, text=item_listino['nome'])

        lista_articoli= api_get('/articoli_listino_tipologie/', id_listino = item_listino['id'] )

        lista_tipologie =[]
        for item in lista_articoli:
            if {'id': item['tipologia'], 'nome': item['nome_tipologia']} not in lista_tipologie:
                lista_tipologie.append({'id': item['tipologia'], 'nome': item['nome_tipologia']})

        canvas = tk.Canvas(listino)
        canvas.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(listino, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')

        canvas.configure(yscrollcommand=scrollbar.set)

        frame_inside_canvas = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_inside_canvas, anchor='nw')

        for tipologia in lista_tipologie:
            frame_tipologia = ttk.Frame(frame_inside_canvas)
            frame_tipologia.pack(side='top', fill='x')

            label_tipologia = ttk.Label(frame_tipologia, text=tipologia['nome'])
            label_tipologia.pack(side='left', padx=10)

            riga_nera = tk.Frame(frame_tipologia, height=1, width=300, bg='black')
            riga_nera.pack(side='left', fill='x', expand=True, padx=10)

            frame_buttons = tk.Frame(frame_inside_canvas)
            frame_buttons.pack(side='top', fill='both', expand=True)

            articoli_per_tipologia = [item for item in lista_articoli if item['tipologia'] == tipologia['id']]


            for i, articolo in enumerate(articoli_per_tipologia):
                #if articolo[sfondo] == hex: #TODO
                #    colore = 'black'
                button = ttk.Button(frame_buttons, text=articolo['nome_breve'],
                                    command=functools.partial(insert_order, ordini_treeview, articolo, item_listino['id'], bill, bill_formatted_text))
                button.grid(row=i // 6, column=i % 6, padx=5, pady=5, sticky='w')
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
    # gestisco bill_frame
    # bill e bill_formatted_text vengono inizializzati all'inizio della funzione
    bill.set(0.00)
    totals_label = ttk.Label(bill_frame, text="Totale: ")
    totals_label.pack(side='left', padx=50)

    bill_label = tk.Label(bill_frame, textvariable=bill_formatted_text)
    bill_label.pack(side='left')
    update_bill(ordini_treeview, bill, bill_formatted_text)

    def prepara_salvataggio(ordini_treeview, profile_id, bill, bill_formatted_text):
        valori_ordine = (
            ('id_profilo', profile_id),
            ('nome_cliente', str(cliente_name.get())),
            ('coperti', str(coperti_name.get())),
            ('tavolo', str(tavolo_name.get())),
            ('note_ordine', str(note_ordine_name.get())),
            ('asporto', str(asporto_value.get())),
            ('veloce', str(veloce_value.get())),
            ('omaggio',str(omaggio_value.get())),
            ('servizio', str(servizio_value.get()))
        )
        salva(ordini_treeview, valori_ordine, bill, bill_formatted_text)
    salva_tutto = ttk.Button(bill_frame, text="Salva", command=functools.partial(prepara_salvataggio, ordini_treeview, profile['id'], bill, bill_formatted_text))
    salva_tutto.pack(side='bottom', pady=(0, 60))

    # gestisco options_frame
    asporto_value = tk.BooleanVar()
    veloce_value = tk.BooleanVar()
    omaggio_value = tk.BooleanVar()
    servizio_value = tk.BooleanVar()

    asporto_checkbox = crea_checkbox(options_frame, "Asporto", asporto_value)
    veloce_checkbox = crea_checkbox(options_frame, "Veloce", veloce_value)
    omaggio_checkbox = crea_checkbox(options_frame, "Omaggio", omaggio_value)
    servizio_checkbox = crea_checkbox(options_frame, "Servizio", servizio_value)

    asporto_checkbox.grid(row=0, column=0, sticky='nsw')
    veloce_checkbox.grid(row=0, column=1, sticky='nsw')
    omaggio_checkbox.grid(row=1, column=0, sticky='nsw')
    servizio_checkbox.grid(row=1, column=1, sticky='nsw')
