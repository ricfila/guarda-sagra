import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
import psycopg2  # used for postgresql queries


class Profiles_window(tk.Tk):  # Creates the profile choice window
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')

        initial_text = ttk.Label(self, text='Scegli un profilo:')

        frame = ttk.Frame(self)
        frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        profiles_choice(frame)

        quit_box = ttk.Frame(self)
        quit_row(quit_box, self)

        initial_text.pack()
        frame.pack()
        quit_box.pack(side=BOTTOM)

        self.mainloop()

class Password_window(tk.Toplevel):
    def __init__(self, profile):
        super().__init__()
        self.title('Inserire la password')
        user_text = ttk.Label(self, text=f'Profilo: {profile}')
        password = tk.StringVar()
        password_field = ttk.Entry(self, textvariable=password)
        button_frame = ttk.Frame(self)
        login_button = ttk.Button(button_frame, text="Accedi", command=lambda: password_confirm(profile, password))
        cancel_button = ttk.Button(button_frame, text="Annulla", command=lambda: self.destroy())

        user_text.pack(expand=True, padx=5, pady=5)
        password_field.pack(expand=True, padx=5, pady=5)
        button_frame.pack(expand=True, padx=5, pady=5)

        login_button.pack(side=LEFT, padx=5, pady=5)
        cancel_button.pack(side=LEFT, padx=5, pady=5)

def quit_row(self, parent):
    quit_button = ttk.Button(self,text="Esci", command=lambda: parent.destroy())
    quit_button.pack(side=RIGHT, padx=5, pady=5)

def profiles_choice(self):
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
    profiles.append('Admin')  # Add to profile choice the admin option. #TODO differenzia bottone admin dai normali, e mettilo sempre a capo. inoltre, 2 tipi di admin

    for i, profile in enumerate(profiles):  # Inserts profile choice buttons
        ttk.Button(self,
                   text=profile,
                   command=lambda profile=profile: selected_profile(profile)).grid(row=i // 4,
                                                                                   column=i % 4,
                                                                                   padx=5,
                                                                                   pady=5)
    return self


def selected_profile(profile):
    if profile == 'Admin':
        Password_window(profile)
    else:
        login(profile)


def password_confirm(profile, password):
    entered_password = password.get()
    if entered_password == "p":  # TODO vedi variabile password_from_db

        login(profile, password)
    elif entered_password == "":
        messagebox.showerror('Errore', 'Inserire la password nel campo apposito per proseguire.')
    else:
        messagebox.showerror('Errore', 'Password errata.')

def login(profile, password = None):
    #TODO se c'è una password, chiama il DB per controllare. Poi:
    pass