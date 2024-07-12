import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, colorchooser
import requests
import json
'''

def draw_articoli(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Articoli")
    # definisco struttura-notebook principale
    articoli_notebook = ttk.Notebook(tab)
    articoli_notebook.pack(fill='both', expand=True)

    def add_notebook_frame(notebook, text):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=text)
        return frame

    articoli_frame = add_notebook_frame(articoli_notebook, 'Articoli')
    tipologie_frame = add_notebook_frame(articoli_notebook, 'Tipologie')
    listini_frame = add_notebook_frame(articoli_notebook, 'Listini')

    # articoli_frame
    # tipologie_frame
    tipologias = []

    def choose_color():
        color = colorchooser.askcolor()[1]  # Returns (color_rgb, color_name)
        return color

    def create_tipologia():
        name = name_entry.get().strip()
        if name and selected_color:
            tipologias.append({"name": name, "color": selected_color})
            update_listbox()
            name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Please enter a name and choose a color.")

    def edit_tipologia():
        global selected_index
        if selected_index != -1:
            new_name = name_entry.get().strip()
            if new_name:
                tipologias[selected_index]["name"] = new_name
                update_listbox()
                name_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Error", "Please enter a new name.")
        else:
            messagebox.showwarning("Error", "Select a tipologia to edit.")

    def remove_tipologia():
        global selected_index
        if selected_index != -1:
            del tipologias[selected_index]
            update_listbox()
            name_entry.delete(0, tk.END)
            selected_index = -1
        else:
            messagebox.showwarning("Error", "Select a tipologia to remove.")

    def update_listbox():
        tipologia_listbox.delete(0, tk.END)
        for tipologia in tipologias:
            tipologia_listbox.insert(tk.END, tipologia["name"])

    def on_select(event):
        global selected_index
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            selected_index = index
            tipologia = tipologias[index]
            name_entry.delete(0, tk.END)
            name_entry.insert(0, tipologia["name"])

    def main():
        global selected_color, selected_index

        selected_color = None
        selected_index = -1

        root = tk.Tk()
        root.title("Tipologia Management")

        # Labels and Entry for Tipologia Name
        name_label = tk.Label(root, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(root)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Button to choose color
        color_button = tk.Button(root, text="Choose Color", command=lambda: choose_and_set_color())
        color_button.grid(row=0, column=2, padx=5, pady=5)

        # Listbox to display existing tipologias
        tipologia_listbox = tk.Listbox(root, width=40, height=10)
        tipologia_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Buttons for actions
        create_button = tk.Button(root, text="Create", command=create_tipologia)
        create_button.grid(row=2, column=0, padx=5, pady=5)

        edit_button = tk.Button(root, text="Edit", command=edit_tipologia)
        edit_button.grid(row=2, column=1, padx=5, pady=5)

        remove_button = tk.Button(root, text="Remove", command=remove_tipologia)
        remove_button.grid(row=2, column=2, padx=5, pady=5)

        # Bind listbox selection event
        tipologia_listbox.bind("<<ListboxSelect>>", on_select)

        def choose_and_set_color():
            global selected_color
            selected_color = choose_color()


    # listini_frame
'''