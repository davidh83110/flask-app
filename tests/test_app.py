import pytest
from main import app
from clients import redis_client


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'version' in data
    assert 'date' in data
    assert 'kubernetes' in data


def test_validate_ip(client):
    response = client.post('/v1/tools/validate', json={'ip': '127.0.0.1'})
    assert response.status_code == 200
    assert response.get_json()['status'] is True

    response = client.post('/v1/tools/validate', json={'ip': 'invalid_ip'})
    assert response.status_code == 400
    assert 'message' in response.get_json()


def test_lookup_domain(client):
    response = client.get('/v1/tools/lookup?domain=www.google.com')
    assert response.status_code == 200
    data = response.get_json()
    assert 'addresses' in data
    assert 'client_ip' in data
    assert 'created_at' in data
    assert 'domain' in data

    response = client.get('/v1/tools/lookup?domain=invalid_domain')
    assert response.status_code == 404
    assert 'message' in response.get_json()


def test_query_history(client):
    # Put some queries first in case Redis is empty.
    client.get('/v1/tools/lookup?domain=example.com')
    client.get('/v1/tools/lookup?domain=example.org')

    response = client.get('/v1/history')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_metrics(client):
    response = client.get('/metrics')
    assert response.status_code == 200
