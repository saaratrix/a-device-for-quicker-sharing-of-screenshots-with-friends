import unittest

from ..file_utility import FileUtility, FileValidation


class MyTestCase(unittest.TestCase):

    def test_get_file_extension(self):
        self.assertEqual(FileUtility.get_file_extension("m333o3ou666666u.txt"), ".txt")
        self.assertEqual(FileUtility.get_file_extension("test"), "")

    def test_validate_path_allow_empty(self):
        FileUtility.validate_path("", 100, True)
        self.assertTrue(True)

    def test_validate_path_bad_characters(self):
        test_data = [
            "",
            "../",
            "../test/../dir",
            "/../../../../../test.jpg",
            "folder/subfolder/file",
            "folder\\subfolder\\file",
            "../folder/subfolder\\../file.txt",
            "test.jpg;.asp",
            "file\0name.txt",
            "file:name.txt",
            "file*name.txt",
            "file?name.txt",
            'file"name.txt',
            "file<name.txt",
            "file>name.txt",
            "file|name.txt",
            "..\\file|<name..txt\\:"
        ]

        for input_path in test_data:
            with self.subTest(input_path=input_path):
                with self.assertRaises(ValueError) as context:
                    FileUtility.validate_path(input_path, 100, False)


    def test_validate_path_valid_max_length(self):
        test_cases = [
            # Test cases that should pass without exceptions
            ("filename.png", FileValidation.MAXLENGTH_FILENAME),
            ("00", FileValidation.MAXLENGTH_DATE),
            ("12", FileValidation.MAXLENGTH_DATE),
            ("31", FileValidation.MAXLENGTH_DATE),
            ("abcdefgh", FileValidation.MAXLENGTH_HASH),
            ("abcdefgh", FileValidation.MAXLENGTH_USER_KEY),
        ]

        for path, max_length in test_cases:
            with self.subTest(path=path, max_length=max_length):
                try:
                    FileUtility.validate_path(path, max_length, True)
                except:
                    self.fail(f"sanitize_path({path}, {max_length}) raised ValueError unexpectedly!")

    def test_validate_path_max_invalid_length(self):
        test_cases = [
            # Test cases that should raise ValueError
            ("a" * (FileValidation.MAXLENGTH_FILENAME + 1), FileValidation.MAXLENGTH_FILENAME),
            ("123", FileValidation.MAXLENGTH_DATE),
            ("230930", FileValidation.MAXLENGTH_DATE),
            ("1234567890abcedf1", FileValidation.MAXLENGTH_HASH),
            ("a" * (FileValidation.MAXLENGTH_HASH + 1), FileValidation.MAXLENGTH_HASH),
            ("a" * (FileValidation.MAXLENGTH_USER_KEY + 1), FileValidation.MAXLENGTH_USER_KEY),
        ]

        for path, max_length in test_cases:
            with self.subTest(path=path, max_length=max_length):
                with self.assertRaises(ValueError):
                    FileUtility.validate_path(path, max_length, True)

    def test_file_allowed(self):
        test_cases = [
            "image.png",
            "file_uploads/23/09/29/test/abdefadja_image.png",
            "video.mp4",
            "audio.mp3",
            "archive.zip",
            "3dmodel.obj",
            "texture.dds",
            "webfile.xml",
        ]

        for filename in test_cases:
            with self.subTest(filename=filename):
                self.assertEqual(FileUtility.is_file_allowed(filename), True)

    def test_file_not_allowed(self):
        test_cases = [
            "forbidden.exe",
            "not_allowed.bat",
            "htaccess",
            "nginx.conf",
            "index.html",
            "",
            "      ",
            ".png",
            ".txt",
            "file_uploads/23/09/29/test/",
            "file_uploads/23/09/29/test",
            "file_uploads/23/09/29/test/index.html",
            "test.jpg;.asp"
        ]

        for filename in test_cases:
            with self.subTest(filename=filename):
                self.assertEqual(FileUtility.is_file_allowed(filename), False)


if __name__ == '__main__':
    unittest.main()
