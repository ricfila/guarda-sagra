import tkinter as tk
from tkinter import ttk

def max_4_chars_and_only_digits(string):
    return string.isdigit() and max_4_chars(string)

def max_4_chars(text):
    return len(text) <= 4



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
    join_listini_articoli = [
        [1, 'Listino 1', 1, 'Articolo 1', 'Primi', 5.00],
        [1, 'Listino 1', 2, 'Articolo 2', 'Primi', 6.00],
        [1, 'Listino 1', 3, 'Articolo 3', 'Primi', 5.50],
        [1, 'Listino 1', 4, 'Articolo 4', 'Primi', 6.50],
        [1, 'Listino 1', 5, 'Articolo 5', 'Primi', 7.00],
        [1, 'Listino 1', 6, 'Articolo 6', 'Primi', 7.50],
        [1, 'Listino 1', 7, 'Articolo 7', 'Primi', 8.00],
        [1, 'Listino 1', 8, 'Articolo 8', 'Primi', 8.50],
        [1, 'Listino 1', 9, 'Articolo 9', 'Primi', 9.00],
        [1, 'Listino 1', 10, 'Articolo 10', 'Primi', 9.50],
        [1, 'Listino 1', 11, 'Articolo 11', 'Primi', 10.00],
        [1, 'Listino 1', 12, 'Articolo 12', 'Primi', 10.50],
        [1, 'Listino 1', 13, 'Articolo 13', 'Primi', 11.00],
        [1, 'Listino 1', 14, 'Articolo 14', 'Primi', 11.50],
        [1, 'Listino 1', 15, 'Articolo 15', 'Primi', 12.00],
        [1, 'Listino 1', 16, 'Articolo 16', 'Primi', 12.50],
        [1, 'Listino 1', 17, 'Articolo 17', 'Primi', 13.00],
        [1, 'Listino 1', 18, 'Articolo 18', 'Primi', 13.50],
        [1, 'Listino 1', 19, 'Articolo 19', 'Primi', 14.00],
        [1, 'Listino 1', 20, 'Articolo 20', 'Primi', 14.50],
        [2, 'Listino 2', 1, 'Articolo 1', 'Primi', 5.00],
        [2, 'Listino 2', 2, 'Articolo 2', 'Primi', 6.00],
        [2, 'Listino 2', 3, 'Articolo 3', 'Primi', 5.50],
        [2, 'Listino 2', 4, 'Articolo 4', 'Primi', 6.50],
        [2, 'Listino 2', 5, 'Articolo 5', 'Primi', 7.00],
        [2, 'Listino 2', 6, 'Articolo 6', 'Primi', 7.50],
        [2, 'Listino 2', 7, 'Articolo 7', 'Primi', 8.00],
        [2, 'Listino 2', 8, 'Articolo 8', 'Primi', 8.50],
        [2, 'Listino 2', 9, 'Articolo 9', 'Primi', 9.00],
        [2, 'Listino 2', 10, 'Articolo 10', 'Primi', 9.50],
        [2, 'Listino 2', 11, 'Articolo 11', 'Primi', 10.00],
        [2, 'Listino 2', 12, 'Articolo 12', 'Primi', 10.50],
        [2, 'Listino 2', 13, 'Articolo 13', 'Primi', 11.00],
        [2, 'Listino 2', 14, 'Articolo 14', 'Primi', 11.50],
        [2, 'Listino 2', 15, 'Articolo 15', 'Primi', 12.00],
        [2, 'Listino 2', 16, 'Articolo 16', 'Primi', 12.50],
        [2, 'Listino 2', 17, 'Articolo 17', 'Primi', 13.00],
        [2, 'Listino 2', 18, 'Articolo 18', 'Primi', 13.50],
        [2, 'Listino 2', 19, 'Articolo 19', 'Primi', 14.00],
        [2, 'Listino 2', 20, 'Articolo 20', 'Primi', 14.50],
        [1, 'Listino 1', 1, 'Articolo 1', 'Secondi', 5.0],
        [1, 'Listino 1', 2, 'Articolo 2', 'Secondi', 6.0],
        [1, 'Listino 1', 3, 'Articolo 3', 'Secondi', 5.5],
        [1, 'Listino 1', 4, 'Articolo 4', 'Secondi', 6.5],
        [1, 'Listino 1', 5, 'Articolo 5', 'Secondi', 7.0],
        [1, 'Listino 1', 6, 'Articolo 6', 'Secondi', 7.5],
        [1, 'Listino 1', 7, 'Articolo 7', 'Secondi', 8.0],
        [1, 'Listino 1', 8, 'Articolo 8', 'Secondi', 8.5],
        [1, 'Listino 1', 9, 'Articolo 9', 'Secondi', 9.0],
        [1, 'Listino 1', 10, 'Articolo 10', 'Secondi', 9.5],
        [1, 'Listino 1', 11, 'Articolo 11', 'Secondi', 10.0],
        [1, 'Listino 1', 12, 'Articolo 12', 'Secondi', 10.5],
        [1, 'Listino 1', 13, 'Articolo 13', 'Secondi', 11.0],
        [1, 'Listino 1', 14, 'Articolo 14', 'Secondi', 11.5],
        [1, 'Listino 1', 15, 'Articolo 15', 'Secondi', 12.0],
        [1, 'Listino 1', 16, 'Articolo 16', 'Secondi', 12.5],
        [1, 'Listino 1', 17, 'Articolo 17', 'Secondi', 13.0],
        [1, 'Listino 1', 18, 'Articolo 18', 'Secondi', 13.5],
        [1, 'Listino 1', 19, 'Articolo 19', 'Secondi', 14.0],
        [1, 'Listino 1', 20, 'Articolo 20', 'Secondi', 14.5],
        [2, 'Listino 2', 1, 'Articolo 1', 'Secondi', 5.0],
        [2, 'Listino 2', 2, 'Articolo 2', 'Secondi', 6.0],
        [2, 'Listino 2', 3, 'Articolo 3', 'Secondi', 5.5],
        [2, 'Listino 2', 4, 'Articolo 4', 'Secondi', 6.5],
        [2, 'Listino 2', 5, 'Articolo 5', 'Secondi', 7.0],
        [2, 'Listino 2', 6, 'Articolo 6', 'Secondi', 7.5],
        [2, 'Listino 2', 7, 'Articolo 7', 'Secondi', 8.0],
        [2, 'Listino 2', 8, 'Articolo 8', 'Secondi', 8.5],
        [2, 'Listino 2', 9, 'Articolo 9', 'Secondi', 9.0],
        [2, 'Listino 2', 10, 'Articolo 10', 'Secondi', 9.5],
        [2, 'Listino 2', 11, 'Articolo 11', 'Secondi', 10.0],
        [2, 'Listino 2', 12, 'Articolo 12', 'Secondi', 10.5],
        [2, 'Listino 2', 13, 'Articolo 13', 'Secondi', 11.0],
        [2, 'Listino 2', 14, 'Articolo 14', 'Secondi', 11.5],
        [2, 'Listino 2', 15, 'Articolo 15', 'Secondi', 12.0],
        [2, 'Listino 2', 16, 'Articolo 16', 'Secondi', 12.5],
        [2, 'Listino 2', 17, 'Articolo 17', 'Secondi', 13.0],
        [2, 'Listino 2', 18, 'Articolo 18', 'Secondi', 13.5],
        [2, 'Listino 2', 19, 'Articolo 19', 'Secondi', 14.0],
        [2, 'Listino 2', 20, 'Articolo 20', 'Secondi', 14.5]
    ]  # Fatta da chatgpt :)

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

            frame_articoli = ttk.Frame(canvas)
            canvas.create_window((0, 0), window=frame_articoli, anchor='nw')
            lista_articoli = sorted(list({(item[2], item[3], item[5]) for item in join_listini_articoli
                                          if (item[0] == item_listino[0] and item[4] == tipologia)}))

            for i, articolo in enumerate(lista_articoli):
                ttk.Button(frame_articoli, text=articolo[1], command=lambda nome=articolo[1]: print(nome)).grid(
                    row=i // 6, column=i % 6, padx=5, pady=5)


            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))


    label3 = ttk.Label(bill_frame, text="bill_frame", background='green')
    label3.pack(expand=True, fill='both')


