import unittest
from unittest.mock import patch, MagicMock

from flask import json, jsonify

from src.api import create_app
from tests import definisci_mock

class TestAree(unittest.TestCase):
    app = None
    ds = [
        (1, 'Area 1', '1.00', '0.00'),
        (2, 'Area 2', '0.00', '0.00'),
    ]
    cols = [('id',), ('nome',), ('coperto',), ('asporto',)]

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    @patch('src.api.aree.get_connection')
    def test_get_aree(self, mock_get_connection):
        mock_cursor = definisci_mock(mock_get_connection)

        mock_cursor.fetchall.return_value = self.ds
        mock_cursor.description = self.cols


        with self.app.app_context():
            response = self.client.get('/aree')
            assert response.status_code == 200
            assert response.get_json()[0]['id'] == self.ds[0][0]
            assert response.get_json()[1]['nome'] == self.ds[1][1]

    @patch('src.api.connection.get_connection')
    def test_get_area(self, mock_get_connection):
        mock_cursor = definisci_mock(mock_get_connection)

        mock_cursor.fetchone.return_value = self.ds[0]
        mock_cursor.description = self.cols
        mock_cursor.rowcount = 1

        with self.app.app_context():
            response = self.client.get('/aree/{}'.format(self.ds[0][0]))
            assert response.status_code == 200
            assert response.get_json()['id'] == self.ds[0][0]
            assert response.get_json()['nome'] == self.ds[0][1]


    @patch('src.api.aree.get_connection')
    @patch('src.api.aree.get_area')
    def test_create_area(self, mock_get_area, mock_get_connection):
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            mock_cursor.fetchone.return_value = (1,)
            mock_get_area.return_value = jsonify({'id': 1, 'nome': 'Area1'})

            area_data = {
                'nome': 'Area Test',
                'coperto': 2.0,
                'asporto': 3.0
            }
            response = self.client.post('/aree', data=json.dumps(area_data), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Area1'})

    @patch('src.api.aree.get_connection')
    @patch('src.api.aree.get_area')
    @patch('src.api.aree.exists_element')
    def test_update_area(self, mock_exists_element, mock_get_area, mock_get_connection):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Area1'})

        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            mock_get_area.return_value = jsonify({'id': 1, 'nome': 'Area1 aggiornata'})

            area_data = {
                'nome': 'Area1 aggiornata',
                'coperto': 2.5,
                'asporto': 3.5
            }

            response = self.client.put('/aree/1', data=json.dumps(area_data), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Area1 aggiornata'})

            mock_exists_element.return_value = (False, None)

            response = self.client.put('/aree/2', data=json.dumps(area_data), content_type='application/json')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Area non trovata")

    @patch('src.api.aree.get_connection')
    @patch('src.api.aree.exists_element')
    def test_delete_area(self, mock_exists_element, mock_get_connection):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Area1'})

        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            response = self.client.delete('/aree/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': 1, 'nome': 'Area1'})

            mock_exists_element.return_value = (False, None)

            response = self.client.delete('/aree/2')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Area non trovata")


if __name__ == '__main__':
    unittest.main()
