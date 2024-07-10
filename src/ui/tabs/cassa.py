import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def max_4_chars_and_only_digits(string):
    return string.isdigit() and max_4_chars(string)

def max_4_chars(text):
    return len(text) <= 4


def insert_order(orders, articolo):
    # Check if there are any existing orders with the same articolo[3] (assuming it's a unique identifier)
    matching_items = [item for item in orders.get_children() if orders.item(item)['values'][1] == articolo[3]]

    if matching_items:
        # If there are matching articles, update the first matching item with an incremented first value
        first_matching_item = matching_items[0]
        current_values = orders.item(first_matching_item)['values']
        current_first_value = int(current_values[0])
        new_first_value = current_first_value + 1
        updated_values = (str(new_first_value),) + tuple(current_values[1:])  # Convert to tuple and concatenate
        orders.item(first_matching_item, values=updated_values)
    else:
        # If there are no matching articles, insert a new one with first value '1'
        orders.insert('', 'end', values=('1', articolo[3], articolo[5], ''))





def on_select_delete(event, orders):
    to_delete = orders.selection()[0]
    orders.delete(to_delete)


def on_select_note_edit(event, orders): #click destro per modificare note. "invio" per modificare, "esc" o click fuori per annullare
    region = orders.identify("region", event.x, event.y)
    if region == "cell":
        col = orders.identify_column(event.x)
        item = orders.identify_row(event.y)
        if col == '#4':
            bbox = orders.bbox(item, '#4')

            if bbox:
                x, y, width, height = bbox
                current_value = orders.item(item)['values'][3]
                edit_entry = ttk.Entry(orders, width=20)
                edit_entry.insert(0, current_value)

                def save_edit(event):
                    new_value = edit_entry.get()
                    orders.set(item, '#4', new_value)
                    edit_entry.destroy()

                edit_entry.bind("<Return>", save_edit)

                def cancel_edit(event):
                    edit_entry.destroy()
                    orders.set(item, '#4', current_value)

                edit_entry.bind("<FocusOut>", cancel_edit) #se si vuole salvare clickando al di fuori, modifica in save_edit
                edit_entry.bind("<Escape>", cancel_edit)

                edit_entry.place(x=x, y=y, width=width, height=height)
                edit_entry.focus_set()


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

    lista_listini = sorted(list({(item[0], item[1]) for item in join_listini_articoli}))
    listini_notebook = ttk.Notebook(choices_frame)
    listini_notebook.pack(fill='both', expand=True)

    for item_listino in lista_listini:
        listino = ttk.Frame(listini_notebook)
        listini_notebook.add(listino, text=item_listino[1])
        lista_tipologie = sorted(list({item[4] for item in join_listini_articoli if item[0] == item_listino[0]}))

        for tipologia in lista_tipologie:

            frame_tipologia = ttk.Frame(listino)
            frame_tipologia.pack(side='top', fill='x')

            label_tipologia = ttk.Label(frame_tipologia, text=tipologia)
            label_tipologia.pack(side='left', padx=10)

            riga_nera = tk.Frame(frame_tipologia, height=1, width=300, bg='black')
            riga_nera.pack(side='left', fill='x', expand=True, padx=10)

            frame_canvas = ttk.Frame(listino)
            frame_canvas.pack(side='top', fill='both', expand=True)

            canvas = tk.Canvas(frame_canvas)
            canvas.pack(side = 'left', fill='both', expand=True)

            scrollbar = ttk.Scrollbar(frame_canvas, orient = 'vertical', command = canvas.yview)
            scrollbar.pack(side='right', fill='y')

            canvas.configure(yscrollcommand=scrollbar.set)

            lista_articoli = sorted(list({tuple(item) for item in join_listini_articoli
                                          if (item[0] == item_listino[0] and item[4] == tipologia)}))

            for i, articolo in enumerate(lista_articoli):
                ttk.Button(canvas, text=articolo[3], command=lambda arti = articolo: insert_order(orders, arti)).grid(row=i // 6, column=i % 6, padx=5, pady=5)

            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

    # gestisco order_frame

    orders = ttk.Treeview(order_frame, columns=('qta', 'piatto', 'prezzo', 'note'), show='headings')
    orders.heading('qta', text='Qtà')
    orders.heading('piatto', text='Piatto')
    orders.heading('prezzo', text='Prezzo')
    orders.heading('note', text='Note')

    orders.pack(side='left', fill='both', expand=True)
    orders.bind("<Double-1>", lambda event, ord=orders: on_select_delete(event, ord))
    orders.bind("<Button-3>", lambda event, ord=orders: on_select_note_edit(event, ord)) #click destro per modificare note. "invio" per modificare, "esc" per annullare


    label3 = ttk.Label(bill_frame, text="bill_frame", background='green')
    label3.pack(expand=True, fill='both')


