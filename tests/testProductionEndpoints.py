from application.app import my_app as app
import pytest


MOCK_PRODUCTION_DATA = [
        {
            "id": 1,
            "quantity": 100,
            "product_id": 1,
            "date_produced": "2024-09-01",
            "employees": [
                {"id": 1, "name": "Alice Johnson", "position": "Manager"},
                {"id": 2, "name": "Bob Williams", "position": "Worker"}
            ]
        },
        {
            "id": 2,
            "quantity": 200,
            "product_id": 2,
            "date_produced": "2024-09-02",
            "employees": [
                {"id": 3, "name": "Charlie Smith", "position": "Supervisor"},
                {"id": 4, "name": "Eve Davis", "position": "Worker"}
            ]
        },
        {
            "id": 3,
            "quantity": 150,
            "product_id": 3,
            "date_produced": "2024-09-03",
            "employees": [
                {"id": 5, "name": "David Brown", "position": "Technician"},
                {"id": 6, "name": "Fiona Adams", "position": "Worker"}
            ]
        }
    ]


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_db_session(mocker):
    return mocker.patch('services.productionServices.db.session')

def test_save_production(mocker, client):
    mocker.patch.object(client, 'post', return_value=MOCK_PRODUCTION_DATA)
    response = client.post('/production', json=MOCK_PRODUCTION_DATA)
    assert response[0]['id'] == MOCK_PRODUCTION_DATA[0]['id']

def test_find_all_production(mocker, client):
    mocker.patch.object(client, 'get', return_value=MOCK_PRODUCTION_DATA)
    response = client.get('/production')
    assert response[0]['id'] == MOCK_PRODUCTION_DATA[0]['id']

def test_no_production_data(mocker, client):
    mocker.patch.object(client, 'get', return_value=[])
    response = client.get('/production')
    assert response == []


if __name__ == '__main__':
    pytest.main([__file__])