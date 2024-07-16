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
        result = [
            (1, 'Tipologia 1', 1, '#FFFFFF', True),
            (2, 'Tipologia 2', 2, '#00FF00', False)
        ]

        mock_cursor = definisci_mock(mock_get_connection)
        mock_cursor.fetchall.return_value = result
        mock_cursor.description = [('id',), ('nome',), ('posizione',), ('sfondo',), ('visibile',)]


        with self.app.app_context():
            response = self.client.get('/tipologie')
            print(response.get_json())
            assert response.status_code == 200
            assert response.get_json()[0]['nome'] == result[0][1]
            assert response.get_json()[1]['nome'] == result[1][1]

    @patch('src.api.connection.get_connection')
    def test_get_tipologia(self, mock_get_connection):
        result = (1, 'Tipologia 1', 1, '#FFFFFF', True)

        mock_cursor = definisci_mock(mock_get_connection)
        mock_cursor.fetchone.return_value = result
        mock_cursor.description = [('id',), ('nome',), ('posizione',), ('sfondo',), ('visibile',)]
        mock_cursor.rowcount = 1

        with self.app.app_context():
            response = self.client.get('/tipologie/{}'.format(result[0]))
            assert response.status_code == 200
            assert response.get_json()['id'] == result[0]
            assert response.get_json()['nome'] == result[1]


if __name__ == '__main__':
    unittest.main()
