import pytest
import requests


BASE_URL = 'http://127.0.0.1:5000'

def test_add_to_cart():
    # Simulate a user adding an item to the cart
    data = {'item_id': '1', 'restaurant_id': '1', 'user_id': '1'}
    response = requests.post(f'{BASE_URL}/add_to_cart', data=data)
    print(f"Response URL: {response.url}")
    print(f"Response Content: {response.text}")
    # Check if the response is as expected
    assert response.status_code == 200
    expected_url = f'/restaurant_details/{data["restaurant_id"]}/{data["user_id"]}'
    assert response.url.endswith(expected_url)

   
    redirected_response = requests.get(response.url)
     
