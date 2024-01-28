import unittest
from unittest.mock import patch
from flask import Flask
from ..admin_delete import admin_delete_bp, format_day


class TestAdminDelete(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = '/fake/path'
        self.app.register_blueprint(admin_delete_bp)
        self.client = self.app.test_client()

    @patch('server.src.uploads.file_manager.FileManager.delete_directory_recursively')
    def test_delete_year_success(self, delete_dir_recursively_mock):
        delete_dir_recursively_mock.return_value = True
        response = self.client.get('/admin/delete/year/2023')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Success")

    @patch('server.src.uploads.file_manager.FileManager.delete_directory_recursively')
    def test_delete_year_failure(self, delete_dir_recursively_mock):
        delete_dir_recursively_mock.return_value = False
        response = self.client.get('/admin/delete/year/2023')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Failed")

    @patch('server.src.uploads.file_manager.FileManager.delete_directory_recursively')
    def test_delete_month_success(self, mock_delete):
        mock_delete.return_value = True
        year = '2023'
        month = 'March'
        response = self.client.get(f'/admin/delete/year/{year}/month/{month}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Success")

    @patch('server.src.uploads.file_manager.FileManager.delete_directory_recursively')
    def test_delete_month_failure(self, mock_delete):
        mock_delete.return_value = False
        year = '2023'
        month = 'March'
        response = self.client.get(f'/admin/delete/year/{year}/month/{month}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Failed")

    @patch('server.src.uploads.file_manager.FileManager.delete_directory_recursively')
    def test_delete_day_success(self, mock_delete):
        mock_delete.return_value = True
        year = '2023'
        month = 'March'
        day = '5'
        response = self.client.get(f'/admin/delete/year/{year}/month/{month}/day/{day}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Success")

    @patch('server.src.uploads.file_manager.FileManager.delete_directory_recursively')
    def test_delete_day_failure(self, mock_delete):
        mock_delete.return_value = False
        year = '2023'
        month = 'March'
        day = '15'
        response = self.client.get(f'/admin/delete/year/{year}/month/{month}/day/{day}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Failed")

    def test_format_day_single_digit(self):
        for day in range(1, 10):
            self.assertEqual(format_day(str(day)), f"0{day}")

    def test_format_day_double_digit(self):
        self.assertEqual(format_day("10"), "10")
        self.assertEqual(format_day("25"), "25")

    def test_format_day_invalid_input(self):
        # Test that non-numeric input raises a ValueError
        with self.assertRaises(ValueError):
            format_day("invalid")


if __name__ == '__main__':
    unittest.main()