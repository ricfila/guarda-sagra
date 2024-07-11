import tkinter as tk
from tkinter import ttk
import functools
import requests
import json
from config import configs


def salva(orders): #TODO Bisognerebbe anche mettere in sicurezza sta roba, ovvero oltre ai dati che invia normalmente la cassa dovrebbe inviare ad esempio una stringa identificativa della sessione che ha ricevuto dal server al momento del login. Facciamo che ci penseremo più avanti
    pass
    '''
    url = 'http://' + configs['API']['server'] + ':' + configs['API']['port'] + '/ordini'
    data_to_send = []

    for item in orders.get_children():
        item_data = {}
        for column in ('qta', 'piatto', 'prezzo', 'note', 'id_listino', 'id_articolo'):
            item_data[column] = orders.item(item, 'values')[orders['columns'].index(column)]
        data_to_send.append(item_data)

    # Convert data to JSON format
    json_data = json.dumps(data_to_send)

    # Send POST request
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 200:
        print("Data saved successfully!")
    else:
        print(f"Error saving data: {response.status_code} - {response.text}")
    '''

def max_4_chars_and_only_digits(string):
    return string.isdigit() and max_4_chars(string)

def max_4_chars(text):
    return len(text) <= 4


def insert_order(orders, articolo):
    matching_item = next((item for item in orders.get_children() if orders.item(item)['values'][2] == articolo[3]), None)

    if matching_item:
        current_values = orders.item(matching_item)['values']
        new_first_value = int(current_values[1]) + 1
        updated_values = ('-', str(new_first_value),) + tuple(current_values[2:])
        orders.item(matching_item, values=updated_values)
    else:
        orders.insert('', 'end', values=('-','1', articolo[3], articolo[5], '', articolo[0], articolo[2]))
    update_bill(orders)

def on_select(event, orders):
    region = orders.identify("region", event.x, event.y)
    if region == "cell":
        col_index = orders.identify_column(event.x)
        col = orders.column(col_index)['id']
        item = orders.identify_row(event.y)
        if col == 'note':
            on_select_note_edit(orders, item, col_index)
        elif col == 'rimuovi':
            on_select_delete(orders, item)


def on_select_delete(orders, item):
    current_values = orders.item(item, 'values')
    if current_values[1] == '1':
        orders.delete(item)
    else:
        decremented_first_value = int(current_values[1]) - 1
        updated_values = ('-', str(decremented_first_value),) + tuple(current_values[2:])
        orders.item(item, values=updated_values)
    update_bill(orders)



def on_select_note_edit(orders, item, col_index):
    # click destro per modificare note. "invio" per modificare, "esc" o click fuori per annullare
    bbox = orders.bbox(item, 'note')

    if bbox:
        x, y, width, height = bbox
        current_value = orders.item(item, 'values')[int(col_index[1:])-1]
        edit_entry = ttk.Entry(orders, width=width)
        edit_entry.insert(0, current_value)

        def save_edit(event):
            new_value = edit_entry.get()
            orders.set(item, 'note', new_value)
            edit_entry.destroy()

        edit_entry.bind("<Return>", save_edit) # invio

        def cancel_edit(event):
            edit_entry.destroy()
            orders.set(item, 'note', current_value)

        edit_entry.bind("<FocusOut>", cancel_edit) #se si vuole salvare clickando al di fuori, modifica in save_edit
        edit_entry.bind("<Escape>", cancel_edit)

        edit_entry.place(x=x, y=y, width=width, height=height)
        edit_entry.update_idletasks()
        def set_focus():
            edit_entry.focus_set()
        edit_entry.after_idle(set_focus)

def update_bill(orders):
    total_price = 0.0

    for item in orders.get_children():
        price_idx = orders['columns'].index('prezzo')
        qta_idx = orders['columns'].index('qta')
        price_str = orders.item(item, 'values')[price_idx]
        try:
            price = float(price_str)
        except ValueError:
            continue
        qta_str = orders.item(item, 'values')[qta_idx]
        try:
            qta = int(qta_str)
        except ValueError:
            continue

        item_total = price * qta
        total_price += item_total
    bill.set(total_price)
    bill_formatted_text.set(f"€ {bill.get():,.2f}")

def draw_cassa(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Cassa")

    # suddivido in frames:
    info_frame = ttk.Frame(tab)
    order_frame = ttk.Frame(tab)
    bill_frame = ttk.Frame(tab)
    options_frame = ttk.Frame(tab)
    choices_frame = ttk.Frame(tab)

    # configuro la griglia
    tab.columnconfigure((0, 1), weight=1, uniform='a')
    tab.rowconfigure(0, weight=1, uniform='a')
    tab.rowconfigure(1, weight=6, uniform='a')
    tab.rowconfigure(2, weight=2, uniform='a')

    # posiziono i frame
    info_frame.grid(row=0, column=0, sticky='nswe')
    order_frame.grid(row=1, column=0, sticky='nswe')
    bill_frame.grid(row=2, column=0, sticky='nsew')
    options_frame.grid(row=0, column=1, sticky='nsew')
    choices_frame.grid(row=1, column=1, rowspan=2, sticky='nsew')

    # gestisco order_frame

    orders = ttk.Treeview(order_frame,
                          columns=('rimuovi', 'qta', 'piatto', 'prezzo', 'note', 'id_listino', 'id_articolo'),
                          show='headings')
    orders.heading('rimuovi', text='Rimuovi')
    orders.heading('qta', text='Qtà')
    orders.heading('piatto', text='Piatto')
    orders.heading('prezzo', text='Prezzo')
    orders.heading('note', text='Note')

    orders.heading('id_listino', text='')
    orders.heading('id_articolo', text='')

    orders.pack(side='left', fill='both', expand=True)

    orders.column('id_listino', width=0)
    orders.column('id_articolo', width=0)
    orders.bind("<Button-1>", lambda event, ord=orders: on_select(event, ord))

    #click sinistro su nota per modificare. "invio" per modificare, "esc" per annullare. click sinistro su rimuovi per rimuovere

    # suddivido e gestisco info_frame
    n_info_frame = ttk.Frame(info_frame)
    n_info_frame.pack(side='top', expand=True, fill='both')
    s_info_frame = ttk.Frame(info_frame)
    s_info_frame.pack(side='top', expand=True, fill='both')

    # cliente
    cliente_label = ttk.Label(n_info_frame, text="Cliente:")
    cliente_name = tk.StringVar()
    cliente_name_entry = ttk.Entry(n_info_frame, textvariable=cliente_name, width=100)
    cliente_label.pack(side='left', padx=(10, 2))
    cliente_name_entry.pack(side='left', padx=(2, 10))

    # coperti
    coperti_label = ttk.Label(n_info_frame, text="Coperti:")
    coperti_name = tk.StringVar()
    coperti_name_entry = ttk.Entry(n_info_frame, textvariable=coperti_name, validate='key',
                                   validatecommand=(n_info_frame.register(max_4_chars_and_only_digits), '%P'), width=4)
    coperti_label.pack(side='left', padx=(10, 2))
    coperti_name_entry.pack(side='left', padx=(2, 10))

    # tavolo
    tavolo_label = ttk.Label(n_info_frame, text="Tavolo:")
    tavolo_name = tk.StringVar()
    tavolo_name_entry = ttk.Entry(n_info_frame, textvariable=tavolo_name, validate='key',
                                  validatecommand=(n_info_frame.register(max_4_chars), '%P'), width=4)
    tavolo_label.pack(side='left', padx=(10, 2))
    tavolo_name_entry.pack(side='left', padx=(2, 10))

    # note
    note_label = ttk.Label(s_info_frame, text="Note:")
    note_name = tk.StringVar()
    note_name_entry = ttk.Entry(s_info_frame, textvariable=note_name)
    note_label.pack(side='left', padx=(10, 2))
    note_name_entry.pack(side='left', padx=(2, 20), expand=True, fill='x')

    # gestisco choices_frame
    join_listini_articoli = [[1, 'Listino 1', 1, 'Articolo 1', 'Primi', 5.00],[2, 'Listino 2', 10, 'Articolo 10', 'Secondi', 9.5]] ###############################COPIA DA TXT

    lista_listini = sorted({(item[0], item[1]) for item in join_listini_articoli})
    listini_notebook = ttk.Notebook(choices_frame)
    listini_notebook.pack(fill='both', expand=True)

    for item_listino in lista_listini:
        listino = ttk.Frame(listini_notebook)
        listini_notebook.add(listino, text=item_listino[1])
        lista_tipologie = sorted(list({item[4] for item in join_listini_articoli if item[0] == item_listino[0]}))

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

            label_tipologia = ttk.Label(frame_tipologia, text=tipologia)
            label_tipologia.pack(side='left', padx=10)

            riga_nera = tk.Frame(frame_tipologia, height=1, width=300, bg='black')
            riga_nera.pack(side='left', fill='x', expand=True, padx=10)

            frame_buttons = tk.Frame(frame_inside_canvas)
            frame_buttons.pack(side='top', fill='both', expand=True)

            lista_articoli = sorted(list({tuple(item) for item in join_listini_articoli
                                          if (item[0] == item_listino[0] and item[4] == tipologia)}))

            for i, articolo in enumerate(lista_articoli):
                #if articolo[sfondo] == hex: #TODO
                #    colore = 'black'
                button = ttk.Button(frame_buttons, text=articolo[3],
                                    command=functools.partial(insert_order, orders, articolo))
                button.grid(row=i // 6, column=i % 6, padx=5, pady=5)
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
    # gestisco bill_frame
    global bill
    bill = tk.DoubleVar()

    global bill_formatted_text
    bill_formatted_text = tk.StringVar()

    bill.set(0.00)
    totals_label = ttk.Label(bill_frame, text="Totale: ")
    totals_label.pack(side='left', padx=50)

    bill_label = tk.Label(bill_frame, textvariable=bill_formatted_text)
    bill_label.pack(side='left')
    update_bill(orders)

    salva_tutto = ttk.Button(bill_frame, text="Salva", command=salva(orders))
    salva_tutto.pack(side='bottom', pady=(0, 60))

    # gestisco options_frame
    asporto_value = tk.BooleanVar()
    veloce_value = tk.BooleanVar()
    omaggio_value = tk.BooleanVar()
    servizio_value = tk.BooleanVar()

    def toggle_checkbox(event, var):
        var.set(not var.get())

    def crea_checkbox(label_text, var):
        frame = tk.Frame(options_frame, borderwidth=1, relief=tk.RIDGE)

        checkbox = tk.Checkbutton(frame, variable=var, onvalue=True, offvalue=False)
        checkbox.pack(side='left')

        label = tk.Label(frame, text=label_text)
        label.pack(side='left', padx=5)

        frame.bind("<Button-1>", lambda event: toggle_checkbox(event, var))
        label.bind("<Button-1>", lambda event: toggle_checkbox(event, var))

        return frame

    asporto_checkbox = crea_checkbox("Asporto", asporto_value)
    veloce_checkbox = crea_checkbox("Veloce", veloce_value)
    omaggio_checkbox = crea_checkbox("Omaggio", omaggio_value)
    servizio_checkbox = crea_checkbox("Servizio", servizio_value)

    asporto_checkbox.grid(row=0, column=0, sticky='nsw')
    veloce_checkbox.grid(row=0, column=1, sticky='nsw')
    omaggio_checkbox.grid(row=1, column=0, sticky='nsw')
    servizio_checkbox.grid(row=1, column=1, sticky='nsw')

