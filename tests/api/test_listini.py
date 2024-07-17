import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, json, jsonify
from src.api.listini import bp

class TestListini(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.app.register_blueprint(bp)

    @patch('src.api.listini.get_connection')
    @patch('src.api.listini.jason_cur')
    def test_get_listini(self, mock_jason_cur, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            mock_jason_cur.return_value = jsonify([{'id': 1, 'nome': 'Listino1'}])

            response = self.client.get('/listini')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [{'id': 1, 'nome': 'Listino1'}])

    @patch('src.api.listini.exists_element')
    def test_get_listino(self, mock_exists_element):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Listino1'})

        with self.app.app_context():
            response = self.client.get('/listini/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Listino1'})

            mock_exists_element.return_value = (False, None)

            response = self.client.get('/listini/2')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Listino non trovato")

    @patch('src.api.listini.get_connection')
    @patch('src.api.listini.jason_cur')
    def test_get_listini_cassa(self, mock_jason_cur, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            mock_jason_cur.return_value = jsonify([{'id': 1, 'nome': 'Listino1'}])

            response = self.client.get('/listini_cassa/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [{'id': 1, 'nome': 'Listino1'}])

    @patch('src.api.listini.get_connection')
    @patch('src.api.listini.get_listino')
    def test_create_listino(self, mock_get_listino, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1,)

        with self.app.app_context():
            mock_get_listino.return_value = jsonify({'id': 1, 'nome': 'Listino1'})

            listino_data = {'nome': 'Listino Test'}

            response = self.client.post('/listini', data=json.dumps(listino_data), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Listino1'})

    @patch('src.api.listini.get_connection')
    @patch('src.api.listini.get_listino')
    @patch('src.api.listini.exists_element')
    def test_update_listino(self, mock_exists_element, mock_get_listino, mock_get_connection):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Listino1'})
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            mock_get_listino.return_value = jsonify({'id': 1, 'nome': 'Listino1 Aggiornato'})

            listino_data = {'nome': 'Listino1 Aggiornato'}

            response = self.client.put('/listini/1', data=json.dumps(listino_data), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Listino1 Aggiornato'})

            mock_exists_element.return_value = (False, None)

            response = self.client.put('/listini/2', data=json.dumps(listino_data), content_type='application/json')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Listino non trovato")

    @patch('src.api.listini.get_connection')
    @patch('src.api.listini.exists_element')
    def test_delete_listino(self, mock_exists_element, mock_get_connection):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Listino1'})
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            response = self.client.delete('/listini/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Listino1'})

            mock_exists_element.return_value = (False, None)

            response = self.client.delete('/listini/2')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Listino non trovato")
            

if __name__ == '__main__':
    unittest.main()
