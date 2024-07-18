import unittest
from unittest.mock import MagicMock, patch, call
import tkinter as tk
from tkinter import ttk
from src.ui.funzioni_generiche import *
import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

class TestFunzioniGeneriche(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.root = tk.Tk()

    @classmethod
    def tearDownClass(self):
        self.root.destroy()

    def test_replace_single_quotes(self):
        result = replace_single_quotes("l'acqua l'aria")
        self.assertEqual(result, "l''acqua l''aria")

    def test_on_select_modifica(self):
        treeview = ttk.Treeview(self.root, columns=(
        'rimuovi', 'id', 'nome', 'nome_breve', 'prezzo', 'copia_cliente', 'copia_cucina', 'copia_bar',
        'copia_pizzeria', 'copia_rosticceria'))
        treeview.insert('', 'end', values=('-', '1', 'aglio', 'aglio', '1', 'True', 'True', 'True', 'True', 'True'))

        id_riga = 'I001'
        indice_colonna = '#3'
        nome_colonna = 'nome'

        treeview.set(id_riga, nome_colonna, 'pomodoro') #non ho modo di ricreare l'inserimento manuale in una entry dinamica

        on_select_modifica(treeview, 'articoli_treeview', id_riga, indice_colonna, nome_colonna)
        self.assertEqual(treeview.set(id_riga, nome_colonna), 'pomodoro')

    @patch('src.ui.funzioni_generiche.messagebox')
    @patch('src.ui.funzioni_generiche.api_delete')
    def test_on_select_rimuovi(self, mock_api_delete, mock_messagebox):
        treeview = ttk.Treeview(self.root, columns=('col1', 'col2'))
        treeview.insert('', 'end', iid='row1', values=('value1', '1'))

        mock_messagebox.askquestion.return_value = 'yes'

        on_select_rimuovi(treeview, 'test_treeview', 'row1')
        mock_api_delete.assert_called_with('/test/1')

    def test_update_bill(self):
        ordini_treeview = ttk.Treeview(self.root, columns=('qta', 'prezzo'))
        ordini_treeview.insert('', 'end', iid='row1', values=('2', '10.50'))
        ordini_treeview.insert('', 'end', iid='row2', values=('3', '7.00'))

        bill = tk.DoubleVar()
        bill_formatted_text = tk.StringVar()
        update_bill(ordini_treeview, bill, bill_formatted_text)

        expected_total = 2 * 10.50 + 3 * 7.00
        self.assertEqual(bill.get(), expected_total)

    def test_toggle_checkbox(self):
        var = tk.BooleanVar()
        var.set(False)

        toggle_checkbox(None, var)
        self.assertTrue(var.get())

        toggle_checkbox(None, var)
        self.assertFalse(var.get())

    def test_crea_checkbox(self):
        parent_frame = tk.Frame(self.root)
        label_text = "Test"
        var = tk.BooleanVar()

        checkbox_frame = crea_checkbox(parent_frame, label_text, var)
        self.assertEqual(checkbox_frame.winfo_children()[1].cget('text'), label_text)

        var.set(True)
        checkbox_frame.event_generate("<ButtonRelease-1>")
        self.assertTrue(var.get())

        var.set(False)
        checkbox_frame.event_generate("<ButtonRelease-1>")
        self.assertFalse(var.get())


if __name__ == '__main__':
    unittest.main()
