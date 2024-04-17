import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
import sys  # used to end the program
import profiles_logic  # contains the profile logic
import config

class Main_window(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        profiles_logic_window = profiles_logic.create_window(self, handle_profile)
        # self.menu = Menu(self)
        # self.frame1 = Frame1(self)
        self.mainloop()


class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=0.3, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        # create the widgets
        menu_button1 = ttk.Button(self, text='Button 1')
        menu_button2 = ttk.Button(self, text='Button 2')
        menu_button3 = ttk.Button(self, text='Button 3')

        menu_slider1 = ttk.Scale(self, orient='vertical')
        menu_slider2 = ttk.Scale(self, orient='vertical')

        toggle_frame = ttk.Frame(self)
        menu_toggle1 = ttk.Checkbutton(toggle_frame, text='check 1')
        menu_toggle2 = ttk.Checkbutton(toggle_frame, text='check 2')

        entry = ttk.Entry(self)

        # create the grid
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        # place the widgets
        menu_button1.grid(row=0, column=0, sticky='nswe', columnspan=2)
        menu_button2.grid(row=0, column=2, sticky='nswe')
        menu_button3.grid(row=1, column=0, columnspan=3, sticky='nsew')

        menu_slider1.grid(row=2, column=0, rowspan=2, sticky='nsew', pady=20)
        menu_slider2.grid(row=2, column=2, rowspan=2, sticky='nsew', pady=20)

        # toggle layout
        toggle_frame.grid(row=4, column=0, columnspan=3, sticky='nsew')
        menu_toggle1.pack(side='left', expand=True)
        menu_toggle2.pack(side='left', expand=True)

        # entry layout
        entry.place(relx=0.5, rely=0.95, relwidth=0.9, anchor='center')


class Frame1(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.3, y=0, relwidth=0.7, relheight=1)
        Entry(self, 'Entry 1', 'Button 1', 'green')
        Entry(self, 'Entry 2', 'Button 2', 'blue')
        Entry(self, 'Entry 3', 'Button 3', 'green')


class Entry(ttk.Frame):
    def __init__(self, parent, label_text, button_text, label_background):
        super().__init__(parent)

        label = ttk.Label(self, text=label_text, background=label_background)
        button = ttk.Button(self, text=button_text)

        label.pack(expand=True, fill='both')
        button.pack(expand=True, fill='both', pady=10)

        self.pack(side='left', expand=True, fill='both', padx=20, pady=20)

global profile
profiles_logic.Profiles_window('Guarda Sagra', (600, 600))


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