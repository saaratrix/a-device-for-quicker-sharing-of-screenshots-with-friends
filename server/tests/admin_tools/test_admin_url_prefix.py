import os
import unittest
from importlib import reload
from server.src.admin_tools import admin_url_prefix as module


class TestAdminUrlPrefix(unittest.TestCase):
    def test_default_admin_path(self):
        if 'ADMIN_URL' in os.environ:
            del os.environ['ADMIN_URL']

        reload(module)
        self.assertEqual(module.admin_url_prefix, '/admin/')

    def test_custom_admin_path(self):
        expected_path = '/custom_admin/'
        os.environ['ADMIN_URL'] = expected_path

        reload(module)
        self.assertEqual(module.admin_url_prefix, expected_path)
        del os.environ["ADMIN_URL"]


if __name__ == '__main__':
    unittest.main()
