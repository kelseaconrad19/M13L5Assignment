import unittest
from unittest.mock import patch
import requests


class TestOrderAPI(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000"
    ORDER_URL = API_URL + "/orders"
    ORDER_OBJ = {
        "customer_id": 1,
        "products": [
            {"id": 1, "quantity": 2},
            {"id": 2, "quantity": 1}
        ],
        "date": "2024-09-30"
    }

    @patch('requests.get')
    def test_1_find_order(self, mock_get):
        mock_orders = [
            {
                "order_id": 1,
                "customer_id": 1,
                "products": [
                    {"id": 1, "quantity": 2},
                    {"id": 2, "quantity": 1}
                ],
                "date": "2024-09-30"
            },
            {
                "order_id": 2,
                "customer_id": 2,
                "products": [
                    {"id": 3, "quantity": 5}
                ],
                "date": "2024-10-01"
            }
        ]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_orders

        response = requests.get(self.ORDER_URL)

        mock_get.assert_called_once_with(self.ORDER_URL)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), mock_orders)

    @patch('requests.post')
    def test_save_order(self, mock_post):
        mock_response = {
            "order_id": 1,
            "customer_id": self.ORDER_OBJ["customer_id"],
            "products": self.ORDER_OBJ["products"],
            "date": self.ORDER_OBJ["date"]
        }

        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = mock_response

        response = requests.post(self.ORDER_URL, json=self.ORDER_OBJ)

        mock_post.assert_called_once_with(self.ORDER_URL, json=self.ORDER_OBJ)

        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.json(), mock_response)

    @patch('requests.get')
    def test_find_no_orders(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []

        response = requests.get(self.ORDER_URL)

        mock_get.assert_called_once_with(self.ORDER_URL)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), [])




if __name__ == '__main__':
    unittest.main()