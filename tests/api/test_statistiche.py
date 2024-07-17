import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, json
from src.api.statistiche import bp

class TestStatistiche(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.app.register_blueprint(bp)


    @patch('src.api.statistiche.get_connection')
    def test_get_vendite(self, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [
            (1, 'Articolo1', 10, '2023-07-15'),
            (1, 'Articolo1', 5, '2023-07-16'),
            (2, 'Articolo2', 7, '2023-07-15'),
            None
        ]

        with self.app.app_context():
            response = self.client.get('/stats/vendite')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [
                {'id': 1, 'nome': 'Articolo1', 'quantita': [{'data': '2023-07-15', 'qta': 10}, {'data': '2023-07-16', 'qta': 5}]},
                {'id': 2, 'nome': 'Articolo2', 'quantita': [{'data': '2023-07-15', 'qta': 7}]}
            ])

    @patch('src.api.statistiche.get_connection')
    def test_get_vendite_giorno(self, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [
            (1, 'Articolo1', 10),
            (2, 'Articolo2', 5),
            None
        ]

        with self.app.app_context():
            response = self.client.get('/stats/vendite/2023-07-15')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [
                {'id': 1, 'nome': 'Articolo1', 'quantita': 10},
                {'id': 2, 'nome': 'Articolo2', 'quantita': 5}
            ])

    @patch('src.api.statistiche.get_connection')
    @patch('src.api.statistiche.col_names')
    def test_get_servizio(self, mock_col_names, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor
        mock_col_names.return_value = ['data', 'coperti', 'asporto', 'totale']
        mock_cursor.fetchall.return_value = [
            ('2023-07-15', 20, 10, 100),
            ('2023-07-16', 15, 5, 80)
        ]

        with self.app.app_context():
            response = self.client.get('/stats/servizio')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [
                {'data': '2023-07-15', 'coperti': 20, 'asporto': 10, 'totale': 100},
                {'data': '2023-07-16', 'coperti': 15, 'asporto': 5, 'totale': 80}
            ])

    """
    @patch('src.api.statistiche.get_connection')
    def test_get_servizio_giorno(self, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (10, 20, 100)

        with self.app.app_context():
            response = self.client.get('/stats/servizio/2023-07-15')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'asporto': 10, 'coperti': 20, 'totale': 100})
    

    @patch('src.api.statistiche.get_connection')
    def test_get_incasso(self, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ('Contanti', 50),
            ('Carta di credito', 150)
        ]

        with self.app.app_context():
            response = self.client.get('/stats/incasso/2023-07-15')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [
                {'tipo_pagamento': 'Contanti', 'totale': 50},
                {'tipo_pagamento': 'Carta di credito', 'totale': 150}
            ])

    @patch('src.api.statistiche.get_connection')
    def test_get_incasso_cassa(self, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ('Contanti', 30),
            ('Carta di credito', 70)
        ]

        with self.app.app_context():
            response = self.client.get('/stats/incasso/2023-07-15/cassa/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [
                {'tipo_pagamento': 'Contanti', 'totale': 30},
                {'tipo_pagamento': 'Carta di credito', 'totale': 70}
            ])
     """


if __name__ == '__main__':
    unittest.main()
