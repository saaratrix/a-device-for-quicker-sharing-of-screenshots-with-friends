import pytest
from flask import Flask
from server.src.routes.admin_delete import admin_delete_bp, format_day
from server.src.uploads.file_manager import FileManager
from server.src.admin_tools.admin_credentials import auth


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = '/fake/path'
    app.register_blueprint(admin_delete_bp)
    return app.test_client()


@pytest.fixture
def auth_success(monkeypatch):
    monkeypatch.setattr(auth, 'authenticate', lambda x, y: True)


@pytest.fixture
def auth_failure(monkeypatch):
    monkeypatch.setattr(auth, 'authenticate', lambda x, y: False)


@pytest.fixture
def delete_success(monkeypatch):
    monkeypatch.setattr(FileManager, 'delete_date_directory_recursively', lambda x: True)


@pytest.fixture
def delete_failure(monkeypatch):
    monkeypatch.setattr(FileManager, 'delete_date_directory_recursively', lambda x: False)


# Individual tests start here
def test_delete_year_success(client, auth_success, delete_success):
    response = client.get('/admin/delete/year/2023')
    assert response.status_code == 200
    assert response.data.decode() == "Success"


def test_delete_year_failure(client, auth_success, delete_failure):
    response = client.get('/admin/delete/year/2023')
    assert response.status_code == 200
    assert response.data.decode() == "Failed"


def test_delete_year_auth_failure(client, auth_failure):
    response = client.get('/admin/delete/year/2023')
    assert response.status_code == 401


def test_delete_month_success(client, auth_success, delete_success):
    response = client.get('/admin/delete/year/2023/month/March')
    assert response.status_code == 200
    assert response.data.decode() == "Success"


def test_delete_month_failure(client, auth_success, delete_failure):
    response = client.get('/admin/delete/year/2023/month/March')
    assert response.status_code == 200
    assert response.data.decode() == "Failed"


def test_delete_month_auth_failure(client, auth_failure):
    response = client.get('/admin/delete/year/2023/month/March')
    assert response.status_code == 401


def test_delete_day_success(client, auth_success, delete_success):
    response = client.get('/admin/delete/year/2023/month/March/day/5')
    assert response.status_code == 200
    assert response.data.decode() == "Success"


def test_delete_day_failure(client, auth_success, delete_failure):
    response = client.get('/admin/delete/year/2023/month/March/day/15')
    assert response.status_code == 200
    assert response.data.decode() == "Failed"


def test_delete_day_auth_failure(client, auth_failure):
    response = client.get('/admin/delete/year/2023/month/March/day/5')
    assert response.status_code == 401


def test_format_day_single_digit():
    for day in range(1, 10):
        assert format_day(str(day)) == f"0{day}"


def test_format_day_double_digit():
    assert format_day("10") == "10"
    assert format_day("25") == "25"


def test_format_day_invalid_input():
    with pytest.raises(ValueError):
        format_day("invalid")
