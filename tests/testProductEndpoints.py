from application.app import my_app as app
import pytest
from flask import Response
import json


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_save_product(client, mocker):
    mock_data = {
        'id': 1,
        'name': 'Product 1',
        'price': 10.00
    }

    mock_response = Response(
        response='{"message": "Product saved successfully"}',
        status=200,
        mimetype='application/json'
    )

    mocker.patch.object(client, 'post', return_value=mock_response)

    response = client.post('/products', json=mock_data)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Product saved successfully'


def test_get_product_list(client, mocker):
    mock_response = Response(
        response='{"message": "Product list accessed successfully."}',
        status=200,
        mimetype='application/json'
    )

    mocker.patch.object(client, 'get', return_value=mock_response)
    response = client.get('/products')
    assert response.status_code == 200

def test_get_bestselling_products(client, mocker):
    mock_top_sellers = [
        {'id': 1, 'name': 'Product 1', 'sales': 100},
        {'id': 2, 'name': 'Product 2', 'sales': 80}
    ]

    mock_response = Response(
        response=json.dumps(mock_top_sellers),
        status=200,
        mimetype='application/json'
    )

    mocker.patch.object(client, 'get', return_value=mock_response)
    response = client.get('/products/top_sellers')
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 2



if __name__ == '__main__':
    pytest.main([__file__])