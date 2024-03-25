import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
import psycopg2  # used for postgresql queries


def selected_profile(profile, callback):
    if profile == 'Admin':
        password = tk.StringVar()
        password_entry = ttk.Entry(profiles_logic_window, textvariable=password)
        password_entry.grid(row=20, column=20, padx=5, pady=5)
        password_confirm_button = ttk.Button(profiles_logic_window, text="Conferma",
                                             command=lambda: password_confirm(profile, callback, password))
        password_confirm_button.grid(row=21, column=20, padx=5, pady=5)
    else:
        callback(profile)


def password_confirm(profile, callback, password):
    entered_password = password.get()
    password_label.grid(row=20, column=21, padx=5, pady=5)
    if entered_password == "p":  # TODO vedi variabile password_from_db
        callback(
            profile)  # TODO altri modi per accedere come admin? questo sembra facilmente bucabile lanciando la funzione callback("Admin")
    elif entered_password == "":
        password_label.config(
            text="Inserire la password nel campo apposito per proseguire, o selezionare un profilo Cassa #",
            foreground='light grey')
    else:
        password_label.config(text="Password errata.", foreground='red')


def create_profiles_logic_window(root, callback):
    # "main" code
    global profiles_logic_window
    profiles_logic_window = Toplevel(root)  # Creates the profile choice window
    profiles = ['Cassa 1', 'Cassa 2', 'Cassa 3', 'Cassa 4']  # TODO
    '''
    # Connect to DB and load profile names
    conn = psycopg2.connect(database="db_name",
                            host="db_host",
                            user="db_user",
                            password="db_pass",
                            port="12345")
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM casse ORDER BY nome")
    profiles = cursor.fetchall()
    cursor.execute("SELECT password FROM configurazione")
    password_from_db = cursor.fetchall() # TODO integrare funzioni di hashing con salting per non avere funzioni salvate in chiaro su DB.
    conn.close()
    '''
    profiles.append('Admin')  # Add to profile choice the admin option.

    for i, profile in enumerate(profiles):  # Inserts profile choice buttons
        (ttk.Button(profiles_logic_window,
                    text=profile,
                    command=lambda profile=profile, callback=callback: selected_profile(profile, callback))
         .grid(row=i // 4,
               column=i % 4,
               padx=5,
               pady=5))

    global password_label
    password_label = ttk.Label(profiles_logic_window, text="")

    quit_button = ttk.Button(profiles_logic_window,
                             text="Esci",
                             command=lambda: callback("quit"))
    quit_button.grid(row=21, column=20, padx=5, pady=5)

    return profiles_logic_window
