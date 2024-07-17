import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from .ui.funzioni_generiche import api_get
from . import main_window

def open_profiles_window(title, size):
    global logout_value
    logout_value = False

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
    profiles = api_get("/profili")

    for i, profile in enumerate(profiles):  # Inserts profile choice buttons
        ttk.Button(frame,
                   text=profile['nome'],
                   command=lambda prof=profile: profile_selection(profiles_window, prof)).grid(row=i // 4,
                                                                                   column=i % 4,
                                                                                   padx=5,
                                                                                   pady=5)

def profile_selection(profiles_window, profilo_scelto):
    #if profile == 'Admin': #TODO INSERIMENTO PASSWORD
    #    open_login_window(profiles_window, profile)
    #else:
    logout_value = tk.BooleanVar() # creo una variabile da passare a main_window per distinguere tra logout e chiusura
    logout_value.set(False)

    profiles_window.destroy()
    main_app = main_window.Main_window(profilo_scelto, logout_value)
    main_app.mainloop()
    if logout_value.get() == True:
        open_profiles_window('Guarda Sagra', (400, 300))


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


    elif entered_password == "":
        messagebox.showerror('Errore', 'Inserire la password nel campo apposito per proseguire.')
    else:
        messagebox.showerror('Errore', 'Password errata.')

