import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, json, jsonify
from src.api.profili import bp

class TestProfili(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.app.register_blueprint(bp)

    @patch('src.api.profili.get_connection')
    @patch('src.api.profili.jason_cur')
    def test_get_profili(self, mock_jason_cur, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            mock_jason_cur.return_value = jsonify([{'id': 1, 'nome': 'Profilo1'}])

            response = self.client.get('/profili')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [{'id': 1, 'nome': 'Profilo1'}])

    @patch('src.api.profili.exists_element')
    def test_get_profilo(self, mock_exists_element):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Profilo1'})

        with self.app.app_context():
            response = self.client.get('/profili/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Profilo1'})

            mock_exists_element.return_value = (False, None)

            response = self.client.get('/profili/2')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Profilo non trovato")

    @patch('src.api.profili.get_connection')
    @patch('src.api.profili.single_jason_cur')
    def test_crea_profilo(self, mock_single_jason_cur, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1,)

        with self.app.app_context():
            mock_single_jason_cur.return_value = jsonify({'id': 1, 'nome': 'Profilo1'})

            profilo_data = {'nome': 'Profilo Test', 'privilegi': 1, 'area': 1, 'password': 'password', 'arrotonda': True}

            response = self.client.post('/profili', data=json.dumps(profilo_data), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Profilo1'})

    @patch('src.api.profili.get_connection')
    @patch('src.api.profili.single_jason_cur')
    @patch('src.api.profili.exists_element')
    def test_update_profilo(self, mock_exists_element, mock_single_jason_cur, mock_get_connection):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Profilo1'})
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            mock_single_jason_cur.return_value = jsonify({'id': 1, 'nome': 'Profilo1 Aggiornato'})

            profilo_data = {'nome': 'Profilo1 Aggiornato', 'privilegi': 1, 'area': 1, 'password': 'password', 'arrotonda': True}

            response = self.client.put('/profili/1', data=json.dumps(profilo_data), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Profilo1 Aggiornato'})

            mock_exists_element.return_value = (False, None)

            response = self.client.put('/profili/2', data=json.dumps(profilo_data), content_type='application/json')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Profilo non trovato")

    """
    @patch('src.api.profili.get_connection')
    @patch('src.api.profili.exists_element')
    def test_delete_profilo(self, mock_exists_element, mock_get_connection):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Profilo1', 'privilegi': 0})
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            response = self.client.delete('/profili/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Profilo1'})

            mock_exists_element.return_value = (False, None)

            response = self.client.delete('/profili/2')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Profilo non trovato")

            mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Profilo1', 'privilegi': 1})
            mock_cursor.rowcount = 0

            response = self.client.delete('/profili/1')
            self.assertEqual(response.status_code, 403)
            self.assertIn("Impossibile cancellare il profilo amministratore", response.data.decode())

            mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Profilo1', 'privilegi': 0})
            mock_cursor.rowcount = 1

            response = self.client.delete('/profili/1')
            self.assertEqual(response.status_code, 403)
            self.assertIn("Impossibile cancellare il profilo, ci sono 1 ordini collegati ad esso", response.data.decode())
    """


if __name__ == '__main__':
    unittest.main()
