import unittest
from unittest.mock import MagicMock, patch, call
from tkinter import ttk, Tk
from src.ui.funzioni_generiche import *


class TestFunzioniGeneriche(unittest.TestCase):

    def test_replace_single_quotes(self):
        result = replace_single_quotes("O'Neill")
        self.assertEqual(result, "O''Neill")

    @patch('src.ui.funzioni_generiche.requests')
    def test_api_get(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_requests.get.return_value = mock_response

        result = api_get('/test')
        self.assertEqual(result, {"key": "value"})

    @patch('src.ui.funzioni_generiche.requests')
    def test_api_post(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_requests.post.return_value = mock_response

        result = api_post('/test', {"key": "value"})
        self.assertEqual(result, 201)

    @patch('src.ui.funzioni_generiche.requests')
    def test_api_put(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.put.return_value = mock_response

        result = api_put('/test', {"key": "value"})
        self.assertEqual(result, 200)

    @patch('src.ui.funzioni_generiche.requests')
    def test_api_delete(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_requests.delete.return_value = mock_response

        result = api_delete('/test')
        self.assertEqual(result, {"key": "value"})

    def test_on_select_modifica(self):
        root = Tk()
        treeview = ttk.Treeview(root, columns=('col1', 'col2'))
        treeview.insert('', 'end', iid='row1', values=('value1', 'value2'))

        id_riga = 'row1'
        indice_colonna = '#1'
        nome_colonna = 'col1'
        treeview.set(id_riga, nome_colonna, 'new_value')

        def mock_save_edit(event, treeview, nome_treeview, id_riga):
            treeview.set(id_riga, nome_colonna, 'new_value')

        on_select_modifica(treeview, 'test_treeview', id_riga, indice_colonna, nome_colonna)
        self.assertEqual(treeview.set(id_riga, nome_colonna), 'new_value')
        root.destroy()

    @patch('src.ui.funzioni_generiche.messagebox')
    @patch('src.ui.funzioni_generiche.api_delete')
    def test_on_select_rimuovi(self, mock_api_delete, mock_messagebox):
        root = Tk()
        treeview = ttk.Treeview(root, columns=('col1', 'col2'))
        treeview.insert('', 'end', iid='row1', values=('value1', '1'))

        mock_messagebox.askquestion.return_value = 'yes'

        on_select_rimuovi(treeview, 'test_treeview', 'row1')
        mock_api_delete.assert_called_with('/test/1')

        root.destroy()

    def test_update_bill(self):
        root = Tk()
        ordini_treeview = ttk.Treeview(root, columns=('qta', 'prezzo'))
        ordini_treeview.insert('', 'end', iid='row1', values=('2', '10.50'))
        ordini_treeview.insert('', 'end', iid='row2', values=('3', '7.00'))

        bill = tk.DoubleVar()
        bill_formatted_text = tk.StringVar()
        update_bill(ordini_treeview, bill, bill_formatted_text)

        expected_total = 2 * 10.50 + 3 * 7.00
        self.assertEqual(bill.get(), expected_total)

        root.destroy()

    def test_toggle_checkbox(self):
        var = tk.BooleanVar()
        var.set(False)

        toggle_checkbox(None, var)
        self.assertTrue(var.get())

        toggle_checkbox(None, var)
        self.assertFalse(var.get())

    def test_crea_checkbox(self):
        root = Tk()
        parent_frame = tk.Frame(root)
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

        root.destroy()


if __name__ == '__main__':
    unittest.main()
