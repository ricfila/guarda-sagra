import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
import sys  # used to end the program
import profiles_logic  # contains the profile logic
import main_window
import config
import threading
import api

def main(chosen_profile):
    if chosen_profile is None:
        profiles_logic.open_profiles_window('Guarda Sagra', (400, 300))
    else:
        main_app = main_window.Main_window(chosen_profile)
        main_app.mainloop()


if __name__ == "__main__":  # Starts the event loop for the main window
    # Inizializza le configurazioni
    config.init()

    # Avvio thread demone per chiamate api
    thread = threading.Thread(target=api.init_thread, daemon=True)
    thread.start()

    main(None)

'''
def main():
    # DA USARE???
    root = ThemedTk() 
    # Define style
    style = ttk.Style(root)
    style.theme_use('plastik')  # Tema standard: equilux. Temi decenti: equilux (dark), plastik (light)

#Codice usato per modificare i temi. Da mettere in settings
    our_themes = root.get_themes()
    our_themes.sort()
    for t in our_themes:
        theme_menu.add_command(label=t, command=lambda t=t:restyler(t))

    # Style changer
    def restyler(theme):      
        style.theme_use(theme)


    # Non so ancora cosa faccia ma sembra utile. Devo capire come usare ttk
    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")
    l1 = ttk.Label(text="Test", style="BW.TLabel")
    l2 = ttk.Label(text="Test", style="BW.TLabel")
'''
