from src import profiles_logic
from src import config
import threading
from src.api import init_thread
import os

def main():
    # Inizializza le configurazioni
    config.init()

    if os.environ.get('DISPLAY', '') == '' and os.environ.get('PYCHARM_DISPLAY_PORT', '') == '':
        print('Impossibile avviare l\'interfaccia grafica')

        init_thread(host="0.0.0.0")
    else:
        # Avvio thread demone per chiamate api
        thread = threading.Thread(target=init_thread, daemon=True)
        thread.start()

        profiles_logic.open_profiles_window('Guarda Sagra', (400, 300))


if __name__ == "__main__":
    main()

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
