import unittest
from unittest.mock import patch, MagicMock
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


if __name__ == '__main__':
    unittest.main()
