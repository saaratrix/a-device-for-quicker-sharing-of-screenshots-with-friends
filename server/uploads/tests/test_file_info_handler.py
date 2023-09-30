import datetime
import os
import unittest
from unittest.mock import patch
from ..file_info_handler import FileInfoHandler


class TestFileInfoHandler(unittest.TestCase):
    def test_generate_hash(self):
        test_data = [
            (1234, "7w1o1o0fewduaf4f", "woofwuff"),
            (1337, "7a7bbcad9ecfdg9h", "abcdefghi"),
            (123871351, "7r0aancd4o2m4192", "random12"),
            (123456.789, "cm6o5o6m6i6n8sf1", "moomins1"),
            (0, "b162538495f6c768", "12345678"),
        ]

        # Mock the behavior of secrets.choice to produce a predictable pattern

        for input_time, expected_hash, random_text in test_data:
            mock_choices = iter(random_text)
            with patch('secrets.choice', lambda x: next(mock_choices)):
                with self.subTest(input_time=input_time, expected_hash=expected_hash):
                    result = FileInfoHandler.generate_hash(input_time)
                    self.assertEquals(len(result), FileInfoHandler.HASH_LENGTH + FileInfoHandler.HASH_RANDOM_LENGTH)
                    self.assertEqual(result, expected_hash)

    def test_get_uri_path(self):
        test_data = [
            ("000101", "", "file.txt", "00/01/01/file.txt"),
            ("220923", "user123", "pic.png", "22/09/23/user123/pic.png"),
            ("991231", "moomins", "holiday.jpg", "99/12/31/moomins/holiday.jpg"),
            ("210312", "john_doe", "document.pdf", "21/03/12/john_doe/document.pdf"),
            ("190505", "", "notes.md", "19/05/05/notes.md"),
        ]

        for date_formatted, user_key, filename, expected_uri in test_data:
            with self.subTest(date_formatted=date_formatted, user_key=user_key, filename=filename, expected_uri=expected_uri):
                result = FileInfoHandler.get_uri_path(date_formatted, user_key, filename)
                self.assertEqual(result, expected_uri)

    def test_get_date_folder_name(self):
        test_data = [
            (datetime.datetime(year=2000, month=1, day=1), "000101", os.path.join("00", "01", "01")),
            (datetime.datetime(year=2022, month=9, day=23), "220923", os.path.join("22", "09", "23")),
            (datetime.datetime(year=2099, month=12, day=31), "991231", os.path.join("99", "12", "31")),
            (datetime.datetime(year=2100, month=3, day=11), "000311", os.path.join("00", "03", "11")),
        ]

        for input_date, expected_formatted_date, expected_output_folder in test_data:
            with self.subTest(input_date=input_date, expected_formatted_date=expected_formatted_date, expected_output_folder=expected_output_folder):
                result_formatted, result_folder = FileInfoHandler.get_date_folder_name(input_date)
                self.assertTrue(result_formatted, expected_formatted_date)
                self.assertEqual(result_folder, expected_output_folder)

    def test_get_upload_path_without_key(self):
        filename = "test.png"
        root = "root"
        # no key so should not add path
        key = ""
        result_uri, result_upload = FileInfoHandler.get_upload_path(filename, key, root)

        hash_total_length = FileInfoHandler.HASH_LENGTH + FileInfoHandler.HASH_RANDOM_LENGTH
        uri_length = len("00/01/01/") + hash_total_length + len(f"_{filename}")
        self.assertTrue(result_uri.endswith(f"_{filename}"))
        self.assertEqual(len(result_uri), uri_length)

        minimum_length = len(f"{root}/") + uri_length
        # Check the structure of the path
        self.assertTrue(result_upload.startswith(root))
        self.assertTrue(result_upload.endswith(f"_{filename}"))
        self.assertTrue(len(result_upload) >= minimum_length)

    def test_get_upload_path_with_key(self):
        filename = "test.png"
        root = "root"
        # no key so should not add path
        key = "little"
        result_uri, result_upload = FileInfoHandler.get_upload_path(filename, key, root)

        key_part = f"/{key}/"
        hash_total_length = FileInfoHandler.HASH_LENGTH + FileInfoHandler.HASH_RANDOM_LENGTH
        uri_length = len("00/01/01") + len(key_part) + hash_total_length + len(f"_{filename}")
        self.assertTrue(result_uri.endswith(f"_{filename}"))
        self.assertTrue(key_part in result_uri)
        self.assertEqual(len(result_uri), uri_length)

        minimum_length = len(f"{root}/") + uri_length
        # Check the structure of the path
        self.assertTrue(result_upload.startswith(root))
        self.assertTrue(result_upload.endswith(f"_{filename}"))
        self.assertTrue(len(result_upload) >= minimum_length)


    def test_get_filepath_from_request(self):
        root = "root"
        year = "00"
        month = "01"
        day = "01"
        key = "mouse"
        prefix = "abcdef"
        filename = "file.txt"
        result_path, result_filename = FileInfoHandler.get_filepath_from_request(year, month, day, prefix, key, filename, root)

        # Construct the expected path
        expected_filename = f"{prefix}_{filename}"
        expected_path = os.path.join(root, year, month, day, key)
        self.assertEqual(result_path, expected_path)
        self.assertEqual(result_filename, expected_filename)


if __name__ == '__main__':
    unittest.main()
