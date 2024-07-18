import unittest
from unittest.mock import Mock, patch
import tkinter as tk
from tkinter import ttk
from src.ui.cassa import salva, max_4_chars_and_only_digits, insert_order, draw_cassa
import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

def mock_api_post(url, data):
    if url == '/ordini':
        return 201


def mock_api_get(url, id_profilo=None, id_listino=None):
    if url == '/listini_cassa/' and id_profilo == 2:
        return [{'id': 1, 'nome': 'Standard'}, {'id': 3, 'nome': 'Pesce'}]
    elif url == '/articoli_listino_tipologie/' and id_listino == 1:
        return [{'id': 1, 'nome': 'SPAGHETTI AL POMODORO', 'nome_breve': 'SPAGHETTI POMODORO', 'prezzo': '5.50',
                 'sfondo': None, 'tipologia': 1, 'nome_tipologia': 'Primi', 'sfondo_tipologia': None},
                {'id': 2, 'nome': 'SPAGHETTI AL RAGU', 'nome_breve': 'SPAGHETTI RAGU', 'prezzo': '6.00', 'sfondo': None,
                 'tipologia': 1, 'nome_tipologia': 'Primi', 'sfondo_tipologia': None}]
    elif url == '/articoli_listino_tipologie/' and id_listino == 3:
        return [{'id': 1, 'nome': 'SPAGHETTI AL POMODORO', 'nome_breve': 'SPAGHETTI POMODORO', 'prezzo': '5.50',
                 'sfondo': None, 'tipologia': 1, 'nome_tipologia': 'Primi', 'sfondo_tipologia': None},
                {'id': 17, 'nome': 'ACQUA NATURALE', 'nome_breve': 'ACQUA NATURALE', 'prezzo': '1.50', 'sfondo': None,
                 'tipologia': 5, 'nome_tipologia': 'Bevande', 'sfondo_tipologia': None}]


class TestCassaFunctions(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.treeview = ttk.Treeview(self.root)
        self.bill = tk.DoubleVar()
        self.bill_formatted_text = tk.StringVar()

    def tearDown(self):
        self.root.destroy()

    def test_salva(self):
        valori_ordine = [('item1', 'valore1'), ('item2', 'valore2')]
        bill = self.bill
        bill_formatted_text = self.bill_formatted_text

        with patch('src.ui.cassa.api_post', side_effect=mock_api_post):
            salva(self.treeview, valori_ordine, bill, bill_formatted_text)

        # Assertions
        self.assertEqual(len(self.treeview.get_children()), 0)

    def test_max_4_chars_and_only_digits(self):
        self.assertTrue(max_4_chars_and_only_digits('1234'))  # Valid input
        self.assertFalse(max_4_chars_and_only_digits('12345'))  # More than 4 characters
        self.assertFalse(max_4_chars_and_only_digits('abc'))  # Non-digit characters

    def test_insert_order(self):
        # Mock data for testing
        articolo = {'id': 1, 'nome': 'SPAGHETTI AL POMODORO', 'nome_breve': 'SPAGHETTI POMODORO', 'prezzo': '5.50',
                    'sfondo': None, 'tipologia': 1, 'nome_tipologia': 'Primi', 'sfondo_tipologia': None}
        id_listino = 1
        bill = self.bill
        bill_formatted_text = self.bill_formatted_text

        # Mocking the Treeview
        self.treeview.insert = Mock()

        # Testing insert_order function
        insert_order(self.treeview, articolo, id_listino, bill, bill_formatted_text)

        # Assertions
        self.assertEqual(self.treeview.insert.call_count, 1)  # Check if insert was called

    @patch('src.ui.cassa.api_get', side_effect=mock_api_get)
    def test_draw_cassa(self, mock_api_get):
        profile = {'id': 2}
        notebook = ttk.Notebook(self.root)

        draw_cassa(notebook, profile)

        self.assertEqual(notebook.index('end'), 1)

        tab = notebook.nametowidget(notebook.tabs()[0])

        info_frame = tab.winfo_children()[0]
        self.assertIsInstance(info_frame, ttk.Frame)
        bill_frame = tab.winfo_children()[1]
        self.assertIsInstance(bill_frame, ttk.Frame)
        options_frame = tab.winfo_children()[2]
        self.assertIsInstance(options_frame, ttk.Frame)

        ordini_treeview = tab.winfo_children()[3]
        self.assertIsInstance(ordini_treeview, ttk.Treeview)

        listini_notebook = tab.winfo_children()[4]
        self.assertIsInstance(listini_notebook, ttk.Notebook)

        self.assertEqual(len(listini_notebook.tabs()), 2)
        standard_tab = listini_notebook.nametowidget(listini_notebook.tabs()[0])
        pesce_tab = listini_notebook.nametowidget(listini_notebook.tabs()[1])

        self.assertEqual(listini_notebook.tab(standard_tab, 'text'), 'Standard')
        self.assertEqual(listini_notebook.tab(pesce_tab, 'text'), 'Pesce')


if __name__ == '__main__':
    unittest.main()
