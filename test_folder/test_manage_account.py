import http.client
import re


domain = '127.0.0.1:5000'
connection = http.client.HTTPConnection(domain)

def test_manage_account():
    # No fields are left empty
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    body = 'oldpassword=1233&newpassword=1234&address=newaddress&card_number=123212321232&&expiration_date=12/2022&cvv=948'

    connection.request('POST', "/manage_account/1", body=body, headers=headers)

    response = connection.getresponse()
    
    assert response.status == 302  # redirect
    assert re.match(r'^.*user_homepage.*$', dict(response.getheaders()).get('Location', '')) is not None

def test_manage_account_fail():
    # Empty fields
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    body = 'email=moezakbar@hotmail.com&password=1233'

    connection.request('POST', '/manage_account/1', body=body, headers=headers)

    response = connection.getresponse()
    
    text = response.read().decode('utf-8')
    assert response.status == 200  # No redirect
    assert "Invalid account information" in text