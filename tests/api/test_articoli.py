import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, json, jsonify
from src.api.articoli import bp

class TestArticoli(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.app.register_blueprint(bp)

    @patch('src.api.articoli.get_connection')
    @patch('src.api.articoli.jason_cur')
    def test_get_articoli(self, mock_jason_cur, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            mock_jason_cur.return_value = jsonify([{'id': 1, 'nome': 'Articolo1'}])

            response = self.client.get('/articoli')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [{'id': 1, 'nome': 'Articolo1'}])

    @patch('src.api.articoli.get_connection')
    @patch('src.api.articoli.exists_element')
    def test_get_articolo(self, mock_exists_element, mock_get_connection):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Articolo1'})

        with self.app.app_context():
            response = self.client.get('/articoli/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Articolo1'})

            mock_exists_element.return_value = (False, None)

            response = self.client.get('/articoli/2')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Articolo non trovato")

    @patch('src.api.articoli.get_connection')
    @patch('src.api.articoli.jason_cur')
    def test_get_articoli_listino(self, mock_jason_cur, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            mock_jason_cur.return_value = jsonify([{'id': 1, 'nome': 'Articolo1'}])

            response = self.client.get('/articoli_listino/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [{'id': 1, 'nome': 'Articolo1'}])

    @patch('src.api.articoli.get_connection')
    @patch('src.api.articoli.jason_cur')
    def test_get_articoli_listino_tipologie(self, mock_jason_cur, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            mock_jason_cur.return_value = jsonify([{'id': 1, 'nome': 'Articolo1', 'nome_tipologia': 'Tipologia1'}])

            response = self.client.get('/articoli_listino_tipologie/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [{'id': 1, 'nome': 'Articolo1', 'nome_tipologia': 'Tipologia1'}])

    @patch('src.api.articoli.get_connection')
    @patch('src.api.articoli.get_articolo')
    def test_create_articolo(self, mock_get_articolo, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            mock_cursor.fetchone.return_value = (1,)
            mock_get_articolo.return_value = jsonify({'id': 1, 'nome': 'Articolo1'})

            articolo_data = {
                'nome': 'Articolo Test',
                'nome_breve': 'Art Test',
                'prezzo': 10.0,
                'copia_cliente': True,
                'copia_cucina': True,
                'copia_bar': True,
                'copia_pizzeria': True,
                'copia_rosticceria': True
            }

            response = self.client.post('/articoli', data=json.dumps(articolo_data), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Articolo1'})

    @patch('src.api.articoli.get_connection')
    @patch('src.api.articoli.get_articolo')
    @patch('src.api.articoli.exists_element')
    def test_update_articolo(self, mock_exists_element, mock_get_articolo, mock_get_connection):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Articolo1'})

        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            mock_get_articolo.return_value = jsonify({'id': 1, 'nome': 'Articolo1 aggiornato'})

            articolo_data = {
                'nome': 'Articolo1 aggiornato',
                'nome_breve': 'Art Agg',
                'prezzo': 15.0,
                'copia_cliente': True,
                'copia_cucina': True,
                'copia_bar': True,
                'copia_pizzeria': True,
                'copia_rosticceria': True
            }

            response = self.client.put('/articoli/1', data=json.dumps(articolo_data), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Articolo1 aggiornato'})

            mock_exists_element.return_value = (False, None)

            response = self.client.put('/articoli/2', data=json.dumps(articolo_data), content_type='application/json')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Articolo non trovato")

    @patch('src.api.articoli.get_connection')
    @patch('src.api.articoli.exists_element')
    def test_delete_articolo(self, mock_exists_element, mock_get_connection):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Articolo1'})

        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            response = self.client.delete('/articoli/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Articolo1'})

            mock_exists_element.return_value = (False, None)

            response = self.client.delete('/articoli/2')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Articolo non trovato")


if __name__ == '__main__':
    unittest.main()
