import pytest
from src.api import create_app


class TestProfili:
    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        with app.test_client() as client:
            with app.app_context():
                yield client

    def test_get_profili(self, client):
        data = [[1, 'admin', 1, None, 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec', None], [2, 'Cassa1', 2, None, None, None], [3, 'Cassa2', 2, 2, None, '0.50']]

        # Esegui una richiesta al client di test
        response = client.get('/profili')

        # Verifica che la risposta sia corretta
        assert response.status_code == 200
        assert response.get_json() == data

    @pytest.mark.parametrize("cassa,listini", [
        (2, [[1, "Standard"], [3, "Pesce"]]),
        (3, [[2, "Panini"]])
    ])
    def test_get_listini_cassa(self, client, cassa, listini):
        response = client.get('/listini_cassa/' + str(cassa))

        # Verifica che la risposta sia corretta
        assert response.status_code == 200
        assert response.get_json() == listini
