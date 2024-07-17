import tkinter as tk
from tkinter import ttk
from .funzioni_generiche import api_get, api_post, crea_checkbox


def draw_profiles(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Profili")

    profili_notebook = ttk.Notebook(tab)
    profili_notebook.pack(fill='both', expand=True)

    def add_notebook_frame(notebook, text): #TODO sposta in funzioni varie
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=text)
        return frame

    profili_page = add_notebook_frame(profili_notebook, 'Profili')
    aree_page = add_notebook_frame(profili_notebook, 'Aree')
    listini_page = add_notebook_frame(profili_notebook, 'Listini')

    # profili_page
    profili_view = ttk.Frame(profili_page)
    profili_view.pack(fill='both', expand=True)

    nuovo_profilo_frame = ttk.Frame(profili_view)
    nuovo_profilo_frame.pack()

    nuovo_profilo_nome_label = ttk.Label(nuovo_profilo_frame, text="Nome nuovo profilo:")
    nuovo_profilo_nome_label.pack(side='left', padx=10, pady=10)

    nuovo_profilo_nome = tk.StringVar()
    nuovo_profilo_nome_entry = ttk.Entry(nuovo_profilo_frame, textvariable=nuovo_profilo_nome)
    nuovo_profilo_nome_entry.pack(side='left', padx=10, pady=10)

    nuovo_profilo_password_label = ttk.Label(nuovo_profilo_frame, text="Password:")
    nuovo_profilo_password_label.pack(side='left', padx=10, pady=10)

    nuovo_profilo_password = tk.StringVar()
    nuovo_profilo_password_entry = ttk.Entry(nuovo_profilo_frame, textvariable=nuovo_profilo_password)
    nuovo_profilo_password_entry.pack(side='left', padx=10, pady=10)

    privilegio_cassa = tk.BooleanVar()
    privilegio_cassa_checkbox = crea_checkbox(nuovo_profilo_frame, "Cassa", privilegio_cassa)
    privilegio_cassa_checkbox.pack(side='left', padx=5, pady=5)

    privilegio_articoli = tk.BooleanVar()
    privilegio_articoli_checkbox = crea_checkbox(nuovo_profilo_frame, "Articoli", privilegio_articoli)
    privilegio_articoli_checkbox.pack(side='left', padx=5, pady=5)

    privilegio_profili = tk.BooleanVar()
    privilegio_profili_checkbox = crea_checkbox(nuovo_profilo_frame, "Profili", privilegio_profili)
    privilegio_profili_checkbox.pack(side='left', padx=5, pady=5)

    privilegio_report = tk.BooleanVar()
    privilegio_report_checkbox = crea_checkbox(nuovo_profilo_frame, "Report", privilegio_report)
    privilegio_report_checkbox.pack(side='left', padx=5, pady=5)

    '''
    if profile['privilegi'] == 1 or profile['privilegi'] % 2 == 0:
        cassa.draw_cassa(notebook, profile)
    if profile['privilegi'] == 1 or profile['privilegi'] % 3 == 0:
        pass  # Temporaneamente libero
    if profile['privilegi'] == 1 or profile['privilegi'] % 5 == 0:
        articoli.draw_articoli(notebook, profile)  # modifica listini, articoli e tipologie
    if profile['privilegi'] == 1 or profile['privilegi'] % 7 == 0:
        profili.draw_profiles(notebook)  # modifica profili, aree e listini collegati
    if profile['privilegi'] == 1 or profile['privilegi'] % 11 == 0:
        report.draw_report(notebook)
    '''


    # aree_page
    aree_view = ttk.Frame(aree_page)
    aree_view.pack(fill='both', expand=True)

    # listini_page
    listini_view = ttk.Frame(listini_page)
    listini_view.pack(fill='both', expand=True)

