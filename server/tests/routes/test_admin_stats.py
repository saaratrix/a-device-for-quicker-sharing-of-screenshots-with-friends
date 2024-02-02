import pytest

from server.src.admin_tools.admin_credentials import auth
from server.src.routes.admin_stats import get_base_uri, size_to_megabytes, convert_to_presentable_stats
from server.src.app import create_app

admin_prefix = '/mega-secret-admin'


@pytest.fixture
def client(monkeypatch):
    app = create_app('file_uploads', False)
    with app.test_client() as client:
        yield client


def test_overview_route(client, monkeypatch):
    monkeypatch.setattr(auth, 'authenticate', lambda x, y: True)
    response = client.get(f'{admin_prefix}/stats/overview')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert html.startswith('<!DOCTYPE html>')


def test_overview_route_unauthorized(client, monkeypatch):
    monkeypatch.setattr(auth, 'authenticate', lambda x, y: False)
    response = client.get(f'{admin_prefix}/stats/overview')
    assert response.status_code == 401


class BaseUriTest:
    pass

def test_get_base_uri_with_path():
    request = BaseUriTest()
    request.path = f'{admin_prefix}/stats/overview/test'
    base_uri = get_base_uri(request)
    assert base_uri == admin_prefix


def test_get_base_uri_with_base_url():
    expected = f'https://localhost:5000{admin_prefix}'
    request = BaseUriTest()
    request.base_url = f'{expected}/stats/overview/test'
    request.path = ''
    base_uri = get_base_uri(request)
    assert base_uri == expected


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


def test_convert_to_presentable_stats():
    # Test data
    root_stats = {'total_size': 3000000000, 'total_files': 1500}
    year_items = [
        ('19', ({'name': '19', 'total_size': 2000000000, 'total_files': 1000}, [
            ('02', ({'name': '02', 'total_size': 500000000, 'total_files': 300}, [
                ('05', ({'name': '05', 'total_size': 300000000, 'total_files': 200}, [])),
            ])),
        ])),
    ]

    expected_output = {
        'name': 'Overview',
        'size': '2861.023 MB',
        'files': 1500,
        'years': [
            {
                'name': '2019',
                'size': '1907.349 MB',
                'files': 1000,
                'months': [
                    {
                        'name': 'February',
                        'size': '476.837 MB',
                        'files': 300,
                        'days': [
                            {
                                'name': '5',
                                'size': '286.102 MB',
                                'files': 200
                            },
                        ]
                    },
                ]
            },
        ]
    }

    result = convert_to_presentable_stats(root_stats, year_items)

    assert result == expected_output
