import unittest

from server.src.routes.admin_stats import get_base_uri, size_to_megabytes
from ...app import create_app


class TestAdminStats(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # I tried patching the get_overview_stats but alas to no avail so for now we just check doctype.
    def test_overview_route(self):
        response = self.client.get('/admin/stats/overview')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))

    def test_get_base_uri_with_x_original_uri(self):
        headers = {'X-Original-URI': '/admin/stats/overview/test'}
        base_uri = get_base_uri(headers)
        self.assertEqual(base_uri, '/admin')

    def test_get_base_uri_with_request_uri(self):
        headers = {'REQUEST_URI': '/admin/stats/overview/test'}
        base_uri = get_base_uri(headers)
        self.assertEqual(base_uri, '/admin')

    def test_get_base_uri_without_known_headers(self):
        headers = {'Unknown-Header': '/admin/stats/overview/test'}
        # Since the function does not handle the case where neither 'X-Original-URI'
        # nor 'REQUEST_URI' is present, this should raise an AttributeError.
        with self.assertRaises(AttributeError):
            get_base_uri(headers)

    def test_size_to_megabytes_with_zero(self):
        size_in_bytes = 0
        result = size_to_megabytes(size_in_bytes)
        self.assertEqual(result, '0 MB')

    def test_size_to_megabytes_with_exact_megabyte(self):
        size_in_bytes = 2 ** 20  # 1 MB in bytes
        result = size_to_megabytes(size_in_bytes)
        self.assertEqual(result, '1 MB')

    def test_size_to_megabytes_with_one_point_zero_one_megabytes(self):
        size_in_bytes = 1.01 * (2 ** 20)  # 1.01 MB in bytes
        result = size_to_megabytes(size_in_bytes)
        self.assertEqual(result, '1.01 MB')

    def test_size_to_megabytes_with_random_size(self):
        size_in_bytes = 123456789
        result = size_to_megabytes(size_in_bytes)
        self.assertEqual(result, '117.738 MB')


if __name__ == '__main__':
    unittest.main()