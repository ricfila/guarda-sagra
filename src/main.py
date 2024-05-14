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
from api import demone

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
    x = threading.Thread(target=demone, daemon=True)
    x.start()

    main(None)

'''
def main():
    # DA USARE???
    root = ThemedTk() 
    # Define style
    style = ttk.Style(root)
    style.theme_use('plastik')  # Tema standard: equilux. Temi decenti: equilux (dark), plastik (light)



    # Create menu
    root_menu = Menu(root)
    root.config(menu=root_menu)

    # Add menu option
    theme_menu = Menu(root_menu, tearoff=0)
    root_menu.add_cascade(label="Themes", menu=theme_menu)


    root.mainloop()
if __name__ == "__main__":  # Starts the event loop for the main window
    main()


'''

''' #Codice usato per modificare i temi. Da mettere in settings
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

     #WIDGET ESEMPI VARI
    esempio_etichetta = tk.Label(root,
                             text="Gestione stand gastronomico:",
                             font=("Helvetica", 10))
    esempio_etichetta.grid(row=0, column=0, sticky="N", padx=20, pady=10)

    esempio_input = tk.Entry()
    esempio_input.grid(row=1, column=0, sticky="WE", padx=10)

    bottone = tk.Button(text="UN BOTTONE!", command=funzione_bottone)
    bottone.grid(row=2, column=2)
'''
