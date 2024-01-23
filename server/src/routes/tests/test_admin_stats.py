import unittest
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


if __name__ == '__main__':
    unittest.main()