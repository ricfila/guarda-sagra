import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import functools
import requests
import json
from config import configs

def replace_single_quotes(input_string):
    return input_string.replace("'", "''")

def api_url():
    return 'http://' + configs['API']['server'] + ':' + configs['API']['port']

def api_get(query_url, id_profilo = -1, id_listino = -1, id_tipologia = -1):
    request_url = api_url() + query_url

    if id_profilo != -1:
        request_url += str(id_profilo)
    elif id_listino != -1:
        request_url += str(id_listino)
    elif id_tipologia != -1:
        request_url += '/' + str(id_tipologia)

    response = requests.get(request_url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore api_get: {response.status_code} - {response.text}")
def api_post(query_url, data_to_send):
    request_url = api_url() + query_url

    json_data = json.dumps(data_to_send)

    headers = {'Content-Type': 'application/json'}
    response = requests.post(request_url, data=json_data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore api_post: {response.status_code} - {response.text}")


def on_treeview_select(event, treeview_name, treeview, bill=None, bill_formatted_text=None):
    region = treeview.identify("region", event.x, event.y)
    if region == "cell":
        indice_colonna = treeview.identify_column(event.x)
        nome_colonna = treeview.column(indice_colonna)['id']
        id_riga = treeview.identify_row(event.y)

        if treeview_name == 'ordini_treeview':
            if nome_colonna == 'note':
                on_select_modifica(treeview, id_riga, indice_colonna, nome_colonna)
            if nome_colonna == 'rimuovi':
                on_select_rimuovi(treeview, treeview_name, id_riga, bill, bill_formatted_text)

        elif treeview_name == 'tipologie_treeview':
            if nome_colonna == 'rimuovi':
                on_select_rimuovi(treeview, treeview_name, id_riga)
            elif nome_colonna == 'nome':
                on_select_modifica(treeview, id_riga, indice_colonna, nome_colonna)
            elif nome_colonna == 'sfondo':
                #on_select_colore(treeview, id_riga, nome_colonna)
                pass

        elif treeview_name == 'articoli_treeview':
            if nome_colonna == 'rimuovi':
                on_select_rimuovi(treeview, treeview_name, id_riga)
            elif nome_colonna == 'nome':
                on_select_modifica(treeview, id_riga, indice_colonna, nome_colonna)

        elif treeview_name == 'articoli_per_listino':
            if nome_colonna == 'aggiungi_rimuovi':
                pass
                #on_select_inverti(treeview, id_riga, indice_colonna, nome_colonna)

def on_select_rimuovi(treeview, treeview_name, id_riga, bill=None, bill_formatted_text=None):
    if treeview_name == ('ordini_treeview'):
        current_values = treeview.item(id_riga, 'values')
        if current_values[1] == '1':
            treeview.delete(id_riga)
        else:
            decremented_first_value = int(current_values[1]) - 1
            updated_values = ('-', str(decremented_first_value),) + tuple(current_values[2:])
            treeview.item(id_riga, values=updated_values)
        update_bill(treeview, bill, bill_formatted_text)
    else: # non ordini_treeview
        reply = messagebox.askquestion("Elimina riga",
                                       f"Vuoi eliminare la riga " + treeview.item(id_riga, 'values')[1])
        if reply == 'yes':
            # api_delete(treeview.item(id_riga, 'values')['id'])  #TODO DELETE REQUEST API (api_delete è un nome temporaneo, devo passare il valore di id?)
            treeview.delete(id_riga)

def on_select_modifica(treeview, id_riga, indice_colonna, nome_colonna):
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

def refresh_treeview(treeview, api_get_string):
    for riga in treeview.get_children():
        treeview.delete(riga)

    nomi_colonne = treeview["columns"]
    if nomi_colonne[0] == 'rimuovi':
        for valore in api_get(api_get_string):
            valori = ['-']
            for colonna in nomi_colonne[1:]:
                valori.append(valore[colonna])
            treeview.insert('', 'end',
                            values=valori)
    refresh_colori(treeview)
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

def scelta_colore(intestazione, colore):
    colore_temp =colorchooser.askcolor(title = intestazione)[1]
    colore.set(colore_temp)

def toggle_checkbox(event, var):
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

def update_bill(ordini_treeview, bill, bill_formatted_text):
    total_price = 0.0

    for item in ordini_treeview.get_children():
        price_idx = ordini_treeview['columns'].index('prezzo')
        qta_idx = ordini_treeview['columns'].index('qta')
        price_str = ordini_treeview.item(item, 'values')[price_idx]
        try:
            price = float(price_str)
        except ValueError:
            continue
        qta_str = ordini_treeview.item(item, 'values')[qta_idx]
        try:
            qta = int(qta_str)
        except ValueError:
            continue

        item_total = price * qta
        total_price += item_total
    bill.set(total_price)
    bill_formatted_text.set(f"€ {bill.get():,.2f}")