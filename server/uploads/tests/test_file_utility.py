import unittest

from ..file_utility import FileUtility


class MyTestCase(unittest.TestCase):

    def test_get_file_extension(self):
        self.assertEqual(FileUtility.get_file_extension("m333o3ou666666u.txt"), ".txt")
        self.assertEqual(FileUtility.get_file_extension("test"), "")

    def test_sanitize_path(self):
        test_data = [
            ("", ""),
            ("../", ""),
            ("../test/../dir", "testdir"),
            ("folder/subfolder/file", "foldersubfolderfile"),
            ("folder\\subfolder\\file", "foldersubfolderfile"),
            ("../folder/subfolder\\../file.txt", "foldersubfolderfile.txt"),
            ("normalfile.txt", "normalfile.txt"),
        ]

        for input_path, expected in test_data:
            with self.subTest(input_path=input_path, expected=expected):
                result = FileUtility.sanitize_path(input_path)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
