import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from flask import json

from src.api.ordini import format_ordine
from src.api import create_app
from tests import definisci_mock


class TestOrdini(unittest.TestCase):
    app = None
    ds = [
        (1, '2024-10-11', 'Joe', 3),
        (2, '2024-10-11', 'John', None),
    ]
    cols = [('id',), ('data',), ('cliente',), ('coperti',)]

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    @patch('src.api.ordini.get_connection')
    @patch('src.api.ordini.format_ordine')
    def test_get_ordini(self, mock_format_ordine, mock_get_connection):
        # Simulazione del cursor
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 2
        mock_cursor.fetchone.side_effect = [
            (1, 'ordine1', datetime(2024, 7, 17, 15, 30, 45, 123456)),
            (2, 'ordine2', datetime(2024, 7, 17, 16, 30, 45, 654321))
        ]

        # Mock della connessione al database
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        # Mock della funzione format_ordine
        mock_format_ordine.side_effect = [
            {'id': 1, 'nome': 'ordine1', 'ora': datetime(2024, 7, 17, 15, 30, 45)},
            {'id': 2, 'nome': 'ordine2', 'ora': datetime(2024, 7, 17, 16, 30, 45)}
        ]

        # Esegui la richiesta GET
        response = self.client.get('/ordini')

        # Definisci l'output atteso
        expected_response = [
            {'id': 1, 'nome': 'ordine1', 'ora': '2024-07-17 15:30:45'},
            {'id': 2, 'nome': 'ordine2', 'ora': '2024-07-17 16:30:45'}
        ]

        # Verifica la risposta
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)

    @patch('src.api.connection.get_connection')
    def test_get_ordine(self, mock_get_connection):
        mock_cursor = definisci_mock(mock_get_connection)

        mock_cursor.fetchone.return_value = None
        mock_cursor.description = self.cols
        mock_cursor.rowcount = 0

        with self.app.app_context():
            response = self.client.get('/ordini/4')
            assert response.status_code == 404

    def test_format_ordine(self):
        cur = MagicMock()
        cur.description = [('id',), ('nome',), ('ora',)]
        cur.fetchone.return_value = (1, 'ordine1', datetime(2024, 10, 17, 15, 30, 45, 123456))

        expected_result = {
            'id': 1,
            'nome': 'ordine1',
            'ora': datetime(2024, 10, 17, 15, 30, 45)
        }

        result = format_ordine(cur)

        assert result == expected_result

    @patch('src.api.ordini.get_connection')
    @patch('src.api.connection.get_connection')
    def test_create_ordine(self, mock_get_connection, mock_get_connection_ordini):
        mock_cursor = definisci_mock(mock_get_connection)
        mock_cursor_ordini = definisci_mock(mock_get_connection_ordini)

        mock_cursor.fetchone.return_value = self.ds[0]
        mock_cursor.description = self.cols
        mock_cursor_ordini.rownumber = 0
        mock_cursor_ordini.fetchone.return_value = (self.ds[0][0],)

        data = {'nome_cliente': self.ds[0][1],
                'asporto': False,
                'coperti': self.ds[0][3],
                'tavolo': '10',
                'note_ordine': '',
                'id_profilo': 2,
                'omaggio': False,
                'servizio': False,
                'articoli': []}

        with self.app.app_context():
            response = self.client.post('/ordini', data=json.dumps(data), headers={'Content-Type': 'application/json'})
            print(response.data)
            assert response.status_code == 201
            assert response.get_json()['id'] == self.ds[0][0]
            assert response.get_json()['coperti'] == self.ds[0][3]


    @patch('src.api.ordini.get_connection')
    @patch('src.api.ordini.get_ordine')
    def test_create_ordine(self, mock_get_ordine, mock_get_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [
            (1,),  # id_ordine
            (10,),  # prezzo articolo
            (0, 0)  # coperto, asporto
        ]
        mock_cursor.rownumber = 1

        mock_get_connection.return_value.cursor.return_value = mock_cursor

        mock_get_ordine.return_value = {'id': 1, 'nome': 'ordine1'}

        ordine_data = {
            'nome_cliente': 'Cliente Test',
            'asporto': False,
            'coperti': 2,
            'tavolo': 'A1',
            'note_ordine': 'Nessuna nota',
            'id_profilo': 1,
            'omaggio': False,
            'servizio': 1,
            'articoli': [
                {'id_articolo': 1, 'qta': 2, 'note': 'Nessuna nota'}
            ]
        }

        response = self.client.post('/ordini', data=json.dumps(ordine_data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'id': 1, 'nome': 'ordine1'})


    @patch('src.api.ordini.get_connection')
    @patch('src.api.ordini.exists_element')
    def test_delete_ordine(self, mock_exists_element, mock_get_connection):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'ordine1'})

        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        response = self.client.delete('/ordini/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 1, 'nome': 'ordine1'})


    @patch('src.api.ordini.get_connection')
    @patch('src.api.ordini.exists_element')
    def test_delete_ordine_not_found(self, mock_exists_element, mock_get_connection):
        mock_exists_element.return_value = (False, None)

        response = self.client.delete('/ordini/1')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode(), "Ordine non trovato")


if __name__ == '__main__':
    unittest.main()
