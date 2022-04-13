from api import app
from flask import json

from balanced_binary_search_tree import UserStatus


def test_na_ip():
    response = app.test_client().get('/ip_city/10.0.0.0', content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['city'] == 'unknown'


def test_munich_ip():
    response = app.test_client().get('/ip_city/172.16.11.254', content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['city'] == 'munich'


def test_london_IP():
    response = app.test_client().get('/ip_city/192.168.1.1', content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['city'] == 'london'


def test_user_status_paying():
    response = app.test_client().get('/user_status/1?date=2017-01-01T10:00:00', content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['user_status'] == UserStatus.PAYING.name


def test_user_status_canceled():
    response = app.test_client().get('/user_status/1?date=2017-02-10T10:00:00', content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['user_status'] == UserStatus.CANCELLED.name


def test_user_status_activated_again():
    response = app.test_client().get('/user_status/1?date=2017-03-10T10:00:00', content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['user_status'] == UserStatus.PAYING.name


def test_user_status_old():
    response = app.test_client().get('/user_status/1?date=2016-10-10T10:00:00', content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['user_status'] == UserStatus.NOT_PAYING.name


def test_transactions():
    response = app.test_client().get('/transactions', content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert len(data) == 5
    assert data[0] == {"city": "london", "user_status": "NOT_PAYING", "product_price": 241.0}
    assert data[1] == {"city": "london", "user_status": "PAYING", "product_price": 341.0}
    assert data[2] == {"city": "munich", "user_status": "NOT_PAYING", "product_price": 541.0}
    assert data[3] == {"city": "munich", "user_status": "PAYING", "product_price": 20.5}
    assert data[4] == {"city": "unknown", "user_status": "CANCELLED", "product_price": 541.0}

