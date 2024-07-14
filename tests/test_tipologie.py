import unittest
from unittest.mock import patch, MagicMock
from src.api import create_app
from . import definisci_mock


class TestTipologie(unittest.TestCase):

    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    @patch('src.api.tipologie.get_connection')
    def test_get_tipologie(self, mock_get_connection):
        mock_cursor = definisci_mock(mock_get_connection)

        mock_cursor.fetchall.return_value = [
            (1, 'Tipologia 1', 1, '#FFFFFF', True),
            (2, 'Tipologia 2', 2, '#00FF00', False)
        ]
        mock_cursor.description = [('id',), ('nome',), ('posizione',), ('sfondo',), ('visibile',)]


        with self.app.app_context():
            response = self.client.get('/tipologie')
            assert response.status_code == 200
            assert response.get_json()[0]['nome'] == 'Tipologia 1'
            assert response.get_json()[1]['nome'] == 'Tipologia 2'

    @patch('src.api.tipologie.get_connection')
    def test_get_tipologia(self, mock_get_connection):
        mock_cursor = definisci_mock(mock_get_connection)

        mock_cursor.fetchone.return_value = (1, 'Tipologia 1', 1, '#FFFFFF', True)
        mock_cursor.description = [('id',), ('nome',), ('posizione',), ('sfondo',), ('visibile',)]

        with self.app.app_context():
            response = self.client.get('/tipologie/1')
            assert response.status_code == 200
            assert response.get_json()['id'] == 1
            assert response.get_json()['nome'] == 'Tipologia 1'


if __name__ == '__main__':
    unittest.main()
