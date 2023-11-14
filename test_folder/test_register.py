import http.client
import re


domain = '127.0.0.1:5000'
connection = http.client.HTTPConnection(domain)

def test_user_register():
    # fill out form with valid email/password. 
    # if this pytest was run before, this test will fail, as the user with this information now exists.
    # if so, DELETE THIS USER FROM DATABASE

    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    body = 'email=newemail@gmail.com&password=1233&name=newname&address=newaddress&card_number=123212321232&&expiration_date=12/2022&cvv=948'

    connection.request('POST', '/register_page', body=body, headers=headers)

    response = connection.getresponse()
    
    assert response.status == 302  # redirect
    assert re.match(r'^.*user_homepage.*$', dict(response.getheaders()).get('Location', '')) is not None

def test_user_register_fail():
    # Email already exists.
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    body = 'email=moezakbar@hotmail.com&password=1233'

    connection.request('POST', '/register_page', body=body, headers=headers)

    response = connection.getresponse()
    
    text = response.read().decode('utf-8')
    assert response.status == 200  # No redirect
    assert "Invalid registration information" in text

def test_user_register_failed2():
    #  Password or email field left empty. In this case, password is empty.
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    body = 'email=nopassword@gmail.com'

    connection.request('POST', '/register_page', body=body, headers=headers)

    response = connection.getresponse()
    text = response.read().decode('utf-8')
    assert response.status == 200  # No redirect
    assert "Invalid registration information" in text