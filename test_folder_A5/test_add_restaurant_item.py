import pytest
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_item_get_request(client):
    # Test GET request
    response = client.get('/addItem/1')  
    assert response.status_code == 200


@patch('app.db')
def test_add_item_post_success(mock_cursor, client):
    mock_cursor_instance = mock_cursor.return_value
    mock_cursor_instance.__enter__.return_value.execute.return_value = None

    # Simulate POST request with valid data
    data = {'name': 'New Dish', 'price': '15.99', 'image_url': 'https://www.allrecipes.com/thmb/GvGzAzmqmTiCFP9AIisrHZav_Gw=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Copycat-Burger-and-Fries-2000-b09140d301434155bda5a8c8a40f5e95.jpeg', 'restaurant_id_fk': 1}
    response = client.post('/add_to_cart', data={'item_id': 1, 'restaurant_id': 1, 'user_id': 1})
    assert response.status_code == 302
  
