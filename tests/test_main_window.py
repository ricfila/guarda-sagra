import unittest
import tkinter as tk
from unittest.mock import MagicMock, patch
from src import main_window

from src import config
import threading
from src.api import init_thread



class TestMainWindow(unittest.TestCase):

    def setUp(self):
        config.init()
        thread = threading.Thread(target=init_thread, daemon=True)
        thread.start()

        self.profile = {'area': None, 'arrotonda': None, 'id': 2, 'nome': 'Cassa1', 'password': None, 'privilegi': 10}

        self.logout_value = MagicMock(spec=tk.BooleanVar)
        self.logout_value.set.return_value = False

        self.window = main_window.Main_window(self.profile, self.logout_value)

    def test_title(self):
        self.assertEqual(self.window.title(), (f'Guarda Sagra - ' +  self.profile["nome"]))

    def test_notebook_tabs(self):
        notebook = self.window.winfo_children()[0]
        tabs = notebook.tabs()
        tab_titles = [notebook.tab(tab_id, option='text') for tab_id in tabs]

        if self.profile['privilegi'] == 1 or self.profile['privilegi'] % 2 == 0:
            self.assertIn('Cassa', tab_titles)
        if self.profile['privilegi'] == 1 or self.profile['privilegi'] % 5 == 0:
            self.assertIn('Articoli', tab_titles)
        if self.profile['privilegi'] == 1 or self.profile['privilegi'] % 7 == 0:
            self.assertNotIn('Profili', tab_titles)
        if self.profile['privilegi'] == 1 or self.profile['privilegi'] % 11 == 0:
            self.assertNotIn('Report', tab_titles)

    def test_logout(self):
        main_window.logout(self.window, self.logout_value)
        self.logout_value.set.assert_called_once_with(True)
        try:
            widget_exists = self.window.winfo_exists()
            self.assertFalse(widget_exists)
        except tk.TclError:
            self.assertTrue(True, "Widget distrutto correttamente")



if __name__ == '__main__':
    unittest.main()
