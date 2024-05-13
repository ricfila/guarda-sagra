import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
import psycopg2  # used for postgresql queries
from main import main
def open_profiles_window(title, size):
    profiles_window = tk.Tk()
    profiles_window.title(title)
    profiles_window.geometry(f'{size[0]}x{size[1]}')
    profiles_window.minsize(size[0], size[1])
    frame = ttk.Frame(profiles_window)
    profiles_choice(profiles_window, frame)

    initial_text = ttk.Label(profiles_window, text='Scegli un profilo:')
    quit_button = ttk.Button(profiles_window, text="Esci", command=lambda: profiles_window.destroy())

    initial_text.pack()
    frame.pack()
    quit_button.place(anchor = 'se', relx = 0.98, rely = 0.98)

    profiles_window.mainloop()



def profiles_choice(profiles_window, frame):
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
    profiles.append('Admin')  # Add to profile choice the admin option. #TODO 2 tipi di admin?

    for i, profile in enumerate(profiles):  # Inserts profile choice buttons
        ttk.Button(frame,
                   text=profile,
                   command=lambda profile=profile: profile_selection(profiles_window, profile)).grid(row=i // 4,
                                                                                   column=i % 4,
                                                                                   padx=5,
                                                                                   pady=5)

def profile_selection(profiles_window, profile):
    if profile == 'Admin':
        open_login_window(profiles_window, profile)
    else:
        profiles_window.destroy()
        main(profile)

def open_login_window(profiles_window, profile):
    login_window = tk.Toplevel()
    login_window.title('Inserire la password')
    password = tk.StringVar()

    user_text = ttk.Label(login_window, text=f'Profilo: {profile}')
    password_field = ttk.Entry(login_window, textvariable=password)

    buttons_frame = ttk.Frame(login_window)
    login_button = ttk.Button(buttons_frame, text="Accedi", command=lambda: password_confirm(profiles_window, profile, password))
    cancel_button = ttk.Button(buttons_frame, text="Annulla", command=lambda: login_window.destroy())

    user_text.pack(expand=True, padx=5, pady=5)
    password_field.pack(expand=True, padx=5, pady=5)
    buttons_frame.pack(expand=True, padx=5, pady=5)
    login_button.pack(side=LEFT, padx=5, pady=5)
    cancel_button.pack(side=LEFT, padx=5, pady=5)

def password_confirm(profiles_window, profile, password):
    entered_password = password.get()
    if entered_password == "p":  # TODO vedi variabile password_from_db
        profiles_window.destroy()
        main(profile)


    elif entered_password == "":
        messagebox.showerror('Errore', 'Inserire la password nel campo apposito per proseguire.')
    else:
        messagebox.showerror('Errore', 'Password errata.')

