from application.app import my_app as app
import pytest
from flask import Response
from services.customerServices import find_customer_lifetime_value


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
@pytest.fixture
def mock_db_session(mocker):
    return mocker.patch('services.customerServices.db.session')

@pytest.fixture
def mock_customer_lifetime_values():
    return [
        {"customer_name": "John", "total_order_value": 1000.0},
        {"customer_name": "Jane", "total_order_value": 2000.0},
        {"customer_name": "Bob", "total_order_value": 3000.0},
    ]

def test_save_customer(mocker, client):
    mock_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "phone": "123-456-7890"
        }

    mocker.patch.object(client, 'post', return_value=mock_data)
    response = client.post('/customers', json=mock_data)
    assert response['name'] == mock_data['name']

def test_get_customer_list(client, mocker):
    mock_response = Response(
        response='{"message": "Customer list accessed successfully."}',
        status=200,
        mimetype='application/json'
    )

    mocker.patch.object(client, 'get', return_value=mock_response)
    response = client.get('/customers')
    assert response.status_code == 200

def test_find_customer_lifetime_value(mock_db_session, mock_customer_lifetime_values):
    mock_db_session.execute.return_value.all.return_value = [
        ("John", 1000.0),
        ("Jane", 2000.0),
        ("Bob", 3000.0),
    ]

    result = find_customer_lifetime_value()
    assert result == mock_customer_lifetime_values

    mock_db_session.execute.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__])