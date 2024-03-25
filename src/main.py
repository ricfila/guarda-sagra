import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
import sys  # used to end the program
import profiles_logic  # contains the profile logic
import config


#provafmjwksnfowen
# Define root
root = ThemedTk()
root.title("Guarda Sagra")  # Root window title
root.withdraw()  # This hides the main window, it's still present it just can't be seen or interacted with

# Define style
style = ttk.Style(root)
style.theme_use('plastik')  # Tema standard: equilux. Temi decenti: equilux (dark), plastik (light)

# Create profiles_logic_window to choose profile
def handle_profile(profile):
    print("Received profile: ", profile) #TODO da rimuovere
    if profile == "quit":
        profiles_logic_window.destroy()  # Removes the toplevel window
        root.destroy()  # Removes the hidden root window
        sys.exit()  # Ends the script
    else:
        root.deiconify()  # Unhides the root window
        root.state('zoomed')  # Apply full-screen on root window
        profiles_logic_window.destroy()  # Removes the toplevel window

profiles_logic_window = profiles_logic.create_profiles_logic_window(root, handle_profile)

# Create menu
root_menu = Menu(root)
root.config(menu=root_menu)

# Add menu option
theme_menu = Menu(root_menu, tearoff=0)
root_menu.add_cascade(label="Themes", menu=theme_menu)

''' #Codice usato per modificare i temi. Da mettere in settings
our_themes = root.get_themes()
our_themes.sort()
for t in our_themes:
    theme_menu.add_command(label=t, command=lambda t=t:restyler(t))

# Style changer
def restyler(theme):      
    style.theme_use(theme)
'''

# Non so ancora cosa faccia ma sembra utile. Devo capire come usare ttk
# style = ttk.Style()
# style.configure("BW.TLabel", foreground="black", background="white")
# l1 = ttk.Label(text="Test", style="BW.TLabel")
# l2 = ttk.Label(text="Test", style="BW.TLabel")

""" #WIDGET ESEMPI VARI
esempio_etichetta = tk.Label(root,
                         text="Gestione stand gastronomico:",
                         font=("Helvetica", 10))
esempio_etichetta.grid(row=0, column=0, sticky="N", padx=20, pady=10)

esempio_input = tk.Entry()
esempio_input.grid(row=1, column=0, sticky="WE", padx=10)

bottone = tk.Button(text="UN BOTTONE!", command=funzione_bottone)
bottone.grid(row=2, column=2)
"""

if __name__ == "__main__":  # Starts the event loop for the main window
    root.mainloop()
