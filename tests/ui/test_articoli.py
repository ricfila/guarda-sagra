import unittest
from unittest.mock import patch, MagicMock, Mock
import tkinter as tk
from tkinter import ttk
from src.ui.articoli import add_to_treeview, add_tipologia



class TestArticoliModule(unittest.TestCase):
    @patch('tkinter.ttk.Treeview')
    @patch('src.ui.articoli.api_post')
    def test_add_to_treeview(self, treeview_mock, mock_api_post):
        mock_api_post.return_value = 201

        add_to_treeview(treeview_mock, 'articoli_treeview', (('nome', 'Nuovo Articolo'), ('prezzo', '10.00')))

        mock_api_post.assert_called_once_with('/articoli', {'nome': 'Nuovo Articolo', 'prezzo': '10.00'})


    @patch('tkinter.ttk.Treeview')
    @patch('src.ui.articoli.api_post')
    def test_add_tipologia(self, treeview_mock, mock_api_post):
        mock_api_post.return_value = 201

        add_tipologia(treeview_mock,
                      (('nome', 'Nuova Tipologia'), ('posizione', '1'), ('sfondo', '#FFFFFF'), ('visibile', True)))

        mock_api_post.assert_called_once_with('/tipologie',
                                              {'nome': 'Nuova Tipologia', 'posizione': '1', 'sfondo': '#FFFFFF',
                                               'visibile': True})



if __name__ == '__main__':
    unittest.main()

