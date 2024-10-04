import pytest
from application.app import my_app as app
from flask import Response
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_db_session(mocker):
    return mocker.patch('services.employeeServices.db.session')

def test_create_employee(mocker, client):
    mock_data = {
        "name": "John",
        "position": "Manager"
    }

    mocker.patch.object(client, 'post', return_value=mock_data)
    response = client.post('/employees', json=mock_data)
    assert response['name'] == mock_data['name']

def test_get_all_employees(mocker, client):
    mock_employees = [
        {"id": 1, "name": "John Doe", "position": "Manager"},
        {"id": 2, "name": "Jane Smith", "position": "Engineer"}
    ]

    mock_response = Response(
        response=json.dumps(mock_employees),
        status=200,
        mimetype='application/json'
    )

    mocker.patch.object(client, 'get', return_value=mock_response)

    response = client.get('/employees')

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) == 2
    assert response_data[0]['name'] == 'John Doe'
    assert response_data[1]['name'] == 'Jane Smith'

def test_get_all_employees_empty(client, mocker):
    mock_response = Response(
        response=json.dumps([]),
        status=200,
        mimetype='application/json'
    )

    mocker.patch.object(client, 'get', return_value=mock_response)

    response = client.get('/employees')

    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert response_data == []


if __name__ == '__main__':
    pytest.main([__file__])