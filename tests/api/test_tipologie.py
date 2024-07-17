import unittest
from unittest.mock import patch, MagicMock

import pytest
from flask import json

from src.api import create_app
from tests import definisci_mock


class TestTipologie(unittest.TestCase):
    app = None
    ds = [
        (1, 'Tipologia 1', 1, '#FFFFFF', True),
        (2, 'Tipologia 2', 2, '#00FF00', False)
    ]
    cols = [('id',), ('nome',), ('posizione',), ('sfondo',), ('visibile',)]

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    @patch('src.api.tipologie.get_connection')
    def test_get_tipologie(self, mock_get_connection):
        mock_cursor = definisci_mock(mock_get_connection)

        mock_cursor.fetchall.return_value = self.ds
        mock_cursor.description = self.cols


        with self.app.app_context():
            response = self.client.get('/tipologie')
            assert response.status_code == 200
            assert response.get_json()[0]['nome'] == self.ds[0][1]
            assert response.get_json()[1]['nome'] == self.ds[1][1]

    @patch('src.api.connection.get_connection')
    def test_get_tipologia(self, mock_get_connection):
        mock_cursor = definisci_mock(mock_get_connection)

        mock_cursor.fetchone.return_value = self.ds[0]
        mock_cursor.description = self.cols
        mock_cursor.rowcount = 1

        with self.app.app_context():
            response = self.client.get('/tipologie/{}'.format(self.ds[0][0]))
            assert response.status_code == 200
            assert response.get_json()['id'] == self.ds[0][0]
            assert response.get_json()['nome'] == self.ds[0][1]

    @patch('src.api.tipologie.get_connection')
    @patch('src.api.connection.get_connection')
    def test_create_tipologia(self, mock_get_connection, mock_get_connection_tipologie):
        mock_cursor = definisci_mock(mock_get_connection)
        definisci_mock(mock_get_connection_tipologie)

        mock_cursor.fetchone.return_value = self.ds[0]
        mock_cursor.description = self.cols
        mock_cursor.rowcount = 1

        with self.app.app_context():
            send = json.dumps(dict(zip([col[0] for col in self.cols], self.ds[0])))
            response = self.client.post('/tipologie', data=send, headers={'Content-Type': 'application/json'})
            assert response.status_code == 201
            assert response.get_json()['id'] == self.ds[0][0]
            assert response.get_json()['nome'] == self.ds[0][1]

    @patch('src.api.tipologie.get_connection')
    @patch('src.api.tipologie.exists_element')
    def test_update_tipologia(self, mock_exists_element, mock_get_connection):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Tipologia1'})
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor
        updated_tipologia = {
            'nome': 'UpdatedTipologia',
            'posizione': 1,
            'sfondo': 'blue',
            'visibile': True
        }

        with self.app.app_context():
            response = self.client.put('/tipologie/1', json=updated_tipologia)
            self.assertEqual(response.status_code, 200)
            mock_cursor.execute.assert_called_with(
                "UPDATE tipologie SET nome = %s, posizione = %s, sfondo = %s, visibile = %s WHERE id = %s;",
                ('UpdatedTipologia', 1, 'blue', True, 1)
            )
            self.assertEqual(response.json['id'], 1)
            self.assertEqual(response.json['nome'], 'Tipologia1')

    @patch('src.api.tipologie.get_connection')
    @patch('src.api.tipologie.exists_element')
    def test_update_tipologia_not_found(self, mock_exists_element, mock_get_connection):
        mock_exists_element.return_value = (False, None)
        with self.app.app_context():
            response = self.client.put('/tipologie/1', json={
                'nome': 'UpdatedTipologia',
                'posizione': 1,
                'sfondo': 'blue',
                'visibile': True
            })
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Tipologia non trovata")

    @patch('src.api.tipologie.get_connection')
    @patch('src.api.tipologie.exists_element')
    def test_delete_tipologia(self, mock_exists_element, mock_get_connection):
        mock_exists_element.return_value = (True, {'id': 1, 'nome': 'Tipologia1'})
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value = mock_cursor

        with self.app.app_context():
            response = self.client.delete('/tipologie/1')
            self.assertEqual(response.status_code, 200)
            mock_cursor.execute.assert_called_with("DELETE FROM tipologie WHERE id = %s", (1,))
            self.assertEqual(response.json['id'], 1)
            self.assertEqual(response.json['nome'], 'Tipologia1')


    @patch('src.api.tipologie.get_connection')
    @patch('src.api.tipologie.exists_element')
    def test_delete_tipologia_not_found(self, mock_exists_element, mock_get_connection):
        mock_exists_element.return_value = (False, None)
        with self.app.app_context():
            response = self.client.delete('/tipologie/1')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Tipologia non trovata")


if __name__ == '__main__':
    unittest.main()
