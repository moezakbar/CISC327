import http.client
import urllib.parse


domain = '127.0.0.1:5000'
connection = http.client.HTTPConnection(domain)
connection.request('GET', '/restaurant_details/1/1')

def test_first_open():
    # test ability to open the page
    response = connection.getresponse()
    assert response.status == 200 # success/OK
    text = response.read().decode('utf-8')
    assert "gOAAt" in text

def test_path1():
    # The item is valid, so the first path is taken and the item is added to cart.
    form_data = urllib.parse.urlencode({
        'item_id': '1',
        'restaurant_id': '1',
        'user_id': '1'
    })

    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    connection.request('POST', '/add_to_cart', form_data, headers) # the form is being submitted with a valid item
    response = connection.getresponse()
    assert response.status == 302 

def test_path2():
    # The user should still be redirected even though the alternate path is taken
    form_data = urllib.parse.urlencode({
        'item_id': '300',
        'restaurant_id': '1',
        'user_id': '1'
    })

    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    connection.request('POST', '/add_to_cart', form_data, headers) # the form is being submitted with an invalid item
    response = connection.getresponse()
    assert response.status == 302 
