import unittest
from unittest.mock import MagicMock, patch, Mock
import tkinter as tk
from tkinter import ttk
from src.ui.cassa import salva, max_4_chars_and_only_digits, insert_order, draw_cassa

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
        self.root = MagicMock()
        self.treeview = MagicMock()
        self.bill = MagicMock()
        self.bill_formatted_text = MagicMock()

    def tearDown(self):
        self.root.destroy()

    def test_salva(self):
        valori_ordine = [('item1', 'valore1'), ('item2', 'valore2')]
        with patch('src.ui.cassa.update_bill') as mock_update_bill:
            with patch('src.ui.cassa.api_post', side_effect=mock_api_post):
                salva(self.treeview, valori_ordine, self.bill, self.bill_formatted_text)

        mock_update_bill.assert_called_once()


    def test_max_4_chars_and_only_digits(self):
        self.assertTrue(max_4_chars_and_only_digits('1234'))  # Valid input
        self.assertFalse(max_4_chars_and_only_digits('12345'))  # More than 4 characters
        self.assertFalse(max_4_chars_and_only_digits('abc'))  # Non-digit characters

    def test_insert_order(self):
        articolo = {'id': 1, 'nome': 'SPAGHETTI AL POMODORO', 'nome_breve': 'SPAGHETTI POMODORO', 'prezzo': '5.50',
                    'sfondo': None, 'tipologia': 1, 'nome_tipologia': 'Primi', 'sfondo_tipologia': None}
        id_listino = 1

        self.treeview.insert = Mock()
        with patch('src.ui.cassa.update_bill') as mock_update_bill:
            insert_order(self.treeview, articolo, id_listino, self.bill, self.bill_formatted_text)

        self.treeview.insert.assert_called_once()

if __name__ == '__main__':
    unittest.main()
