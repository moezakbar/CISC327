# import pytest
import http.client
import re


domain = '127.0.0.1:5000'
connection = http.client.HTTPConnection(domain)
connection.request('GET', '/')


def test_first_open():
    # test ability to open the page
    response = connection.getresponse()
    assert response.status == 200 # success/OK
    text = response.read().decode('utf-8')
    assert "gOAAt" in text

def test_user_login():
    # fill out form with correct email/password
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    body = 'email=moezakbar@hotmail.com&password=1233'

    connection.request('POST', '/', body=body, headers=headers)

    response = connection.getresponse()
    
    assert response.status == 302  # redirect
    assert re.match(r'^.*user_homepage.*$', dict(response.getheaders()).get('Location', '')) is not None

def test_user_login_fail():
    # fill out form with incorrect email/password
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    body = 'email=test@gmail.com&password=111'

    connection.request('POST', '/', body=body, headers=headers)

    response = connection.getresponse()
    text = response.read().decode('utf-8')
    assert response.status == 200  # No redirect
    assert "Invalid email or password" in text

def test_business_login():
    # fill out form with correct email/password, business portal checkbox checked
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    body = 'email=restaurantowner@gmail.com&password=1234&businessPortal=on'

    connection.request('POST', '/', body=body, headers=headers)

    response = connection.getresponse()
    assert response.status == 302  # redirect
    assert re.match(r'^.*restaurant_owner.*$', dict(response.getheaders()).get('Location', '')) is not None

def test_business_login_fail():
    # fill out form with invalid email/password, business portal checkbox checked
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    body = 'email=restaurantowner@gmail.com&password=12345&businessPortal=on'

    connection.request('POST', '/', body=body, headers=headers)

    response = connection.getresponse()
    text = response.read().decode('utf-8')
    assert response.status == 200  # No redirect
    assert "Invalid email or password" in text
    