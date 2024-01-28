import unittest
from unittest.mock import patch
import importlib
import admin_tools.admin_credentials as module


class TestAdminCredentials(unittest.TestCase):
    @patch.dict('os.environ', {'ADMIN_USERNAME': 'sparkle_queen'})
    def test_check_admin_username(self):
        # Reload the module after setting the mock to ensure the environment variable is used.
        importlib.reload(module)

        # Test with the correct username
        self.assertTrue(module.AdminCredentials.check_admin_username('sparkle_queen'))

        # Test with an incorrect username
        self.assertFalse(module.AdminCredentials.check_admin_username('glitter_goddess'))

    def test_check_password_rejects_secret(self):
        import importlib

        importlib.reload(module)
        forbidden_password = "SECRET"
        assert not module.AdminCredentials.check_admin_password(forbidden_password)

    @patch.dict('os.environ', {'ADMIN_PASSWORD': 'test_password'})
    def test_admin_credentials_with_mocked_env_var(self):
        importlib.reload(module)
        assert not module.AdminCredentials.check_admin_password('wrong_password')
        # Your test logic here
        assert module.AdminCredentials.check_admin_password('test_password')
