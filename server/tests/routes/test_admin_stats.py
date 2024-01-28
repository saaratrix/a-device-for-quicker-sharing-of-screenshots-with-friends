import pytest
from unittest.mock import patch

from server.src.admin_tools.admin_credentials import auth
from server.src.routes.admin_stats import get_base_uri, size_to_megabytes
from server.src.app import create_app


@pytest.fixture
def client(monkeypatch):
    app = create_app('file_uploads', False)
    with app.test_client() as client:

        yield client


def test_overview_route(client, monkeypatch):
    monkeypatch.setattr(auth, 'authenticate', lambda x, y: True)
    response = client.get('/admin/stats/overview')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert html.startswith('<!DOCTYPE html>')

def test_overview_route_unauthorized(client, monkeypatch):
    monkeypatch.setattr(auth, 'authenticate', lambda x, y: False)
    response = client.get('/admin/stats/overview')
    assert response.status_code == 401

def test_get_base_uri_with_x_original_uri():
    headers = {'X-Original-URI': '/admin/stats/overview/test'}
    base_uri = get_base_uri(headers)
    assert base_uri == '/admin'

def test_get_base_uri_with_request_uri():
    headers = {'REQUEST_URI': '/admin/stats/overview/test'}
    base_uri = get_base_uri(headers)
    assert base_uri == '/admin'

def test_get_base_uri_without_known_headers():
    headers = {'Unknown-Header': '/admin/stats/overview/test'}
    with pytest.raises(AttributeError):
        get_base_uri(headers)

def test_size_to_megabytes_with_zero():
    size_in_bytes = 0
    result = size_to_megabytes(size_in_bytes)
    assert result == '0 MB'

def test_size_to_megabytes_with_exact_megabyte():
    size_in_bytes = 2 ** 20  # 1 MB in bytes
    result = size_to_megabytes(size_in_bytes)
    assert result == '1 MB'

def test_size_to_megabytes_with_one_point_zero_one_megabytes():
    size_in_bytes = 1.01 * (2 ** 20)  # 1.01 MB in bytes
    result = size_to_megabytes(size_in_bytes)
    assert result == '1.01 MB'

def test_size_to_megabytes_with_random_size():
    size_in_bytes = 123456789
    result = size_to_megabytes(size_in_bytes)
    assert result == '117.738 MB'