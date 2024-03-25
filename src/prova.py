import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class main_window():
    root = tk.Tk()
    root.title("some application")

    button=ttk.Button(root)
    print(button.config())

    root.mainloop()
