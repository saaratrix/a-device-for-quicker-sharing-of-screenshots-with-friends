import os
import unittest
from datetime import datetime

from ..file_info_obfuscated_handler import FileInfoObfuscatedHandler


class TestFileHandler(unittest.TestCase):
    test_files_folder = "test_files"

    file_info_tests = [
        (datetime(2000, 1, 1, 0, 0, 0), "muu", os.path.join("00", "01", "01"), "m333o3ou666666u"),
        (datetime(2104, 6, 12, 13, 11, 50), "muu", os.path.join("04", "06", "12"), "m373gouuvcvvr6u"),
        (datetime(1924, 4, 15, 1, 17, 35), "muu", os.path.join("24", "04", "15"), "mu737oru6vv8cru"),
        (datetime(2050, 5, 10, 0, 0, 0), "muu", os.path.join("50", "05", "10"), "mr33ro3u666666u"),
        (datetime(2078, 7, 11, 5, 47, 42), "muu", os.path.join("78", "07", "11"), "m1w31oou6r0809u"),
        (datetime(2099, 12, 31, 23, 59, 59), "muu", os.path.join("99", "12", "31"), "mffou5ou9cr4r4u")
    ]

    def test_get_file_infos(self):
        for date, random_chars, expected_folder, expected_resource_name in self.file_info_tests:
            folder_path, resource_name = FileInfoObfuscatedHandler.get_file_infos(date, random_chars)
            self.assertEquals(folder_path, expected_folder)
            self.assertEquals(resource_name, expected_resource_name)

    def test_deconstruct_uri(self):
        file_directory = os.path.dirname(os.path.abspath(__file__))
        root = os.path.join(file_directory, self.test_files_folder)

        date, random_chars, expected_folder, uri = self.file_info_tests[0]
        expected_path = os.path.join(self.test_files_folder, expected_folder, f"{uri}.txt")
        path = FileInfoObfuscatedHandler.get_filepath_from_uri(uri, root)
        self.assertTrue(path.endswith(expected_path))

        date, random_chars, expected_folder, uri = self.file_info_tests[5]
        expected_path = os.path.join(self.test_files_folder, expected_folder, uri)
        path = FileInfoObfuscatedHandler.get_filepath_from_uri(uri, root)
        self.assertTrue(path.endswith(expected_path))


if __name__ == '__main__':
    unittest.main()
