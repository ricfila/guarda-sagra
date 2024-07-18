import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import ttk
from src.ui.articoli import add_to_treeview, add_tipologia
import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


class TestArticoliModule(unittest.TestCase):

    @patch('src.ui.articoli.api_post')
    @patch('src.ui.articoli.refresh_treeview')
    def test_add_to_treeview(self, mock_refresh_treeview, mock_api_post):
        mock_api_post.return_value = 201
        treeview_mock = ttk.Treeview(tk.Tk())

        add_to_treeview(treeview_mock, 'articoli_treeview', (('nome', 'Nuovo Articolo'), ('prezzo', '10.00')))

        mock_api_post.assert_called_once_with('/articoli', {'nome': 'Nuovo Articolo', 'prezzo': '10.00'})

        mock_refresh_treeview.assert_called_once_with(treeview_mock, 'articoli_treeview', '/articoli')

    @patch('src.ui.articoli.api_post')
    @patch('src.ui.articoli.refresh_treeview')
    def test_add_tipologia(self, mock_refresh_treeview, mock_api_post):
        mock_api_post.return_value = 201

        treeview_mock = ttk.Treeview(tk.Tk())

        add_tipologia(treeview_mock,
                      (('nome', 'Nuova Tipologia'), ('posizione', '1'), ('sfondo', '#FFFFFF'), ('visibile', True)))

        mock_api_post.assert_called_once_with('/tipologie',
                                              {'nome': 'Nuova Tipologia', 'posizione': '1', 'sfondo': '#FFFFFF',
                                               'visibile': True})

        mock_refresh_treeview.assert_called_once_with(treeview_mock, 'tipologie_treeview', '/tipologie')


if __name__ == '__main__':
    unittest.main()

