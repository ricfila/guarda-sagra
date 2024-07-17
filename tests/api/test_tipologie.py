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


if __name__ == '__main__':
    unittest.main()
