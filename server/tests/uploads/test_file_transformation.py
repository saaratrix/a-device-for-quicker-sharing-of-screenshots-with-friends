import unittest
from unittest.mock import Mock, patch

from werkzeug.datastructures import FileStorage

from server.src.uploads.file_transformation import FileTransformation


class TestFileTransformation(unittest.TestCase):

    #### get_file_type tests
    def test_get_file_type_image_extensions(self):
        test_cases = [
            ("picture.jpg", "image"),
            ("picture.JPG", "image"),
            ("picture.jpeg", "image"),
            ("photo.png", "image"),
            ("scan.TIFF", "image"),
            ("animation.gif", "image"),
            ("image.webp", "image"),
            ("something/file_uploads/xyz/kitty.bmp", "image")
        ]

        for filename, expected in test_cases:
            with self.subTest(filename=filename):
                self.assertEqual(FileTransformation.get_file_type(filename), expected)

    def test_get_file_type_non_images(self):
        test_cases = [
            "video.mp4",
            "document.pdf",
            "archive.zip",
            "music.mp3",
            "unknownfile",
            "no_extension.",
            ".hiddenfile"
        ]

        for filename in test_cases:
            with self.subTest(filename=filename):
                self.assertEqual(FileTransformation.get_file_type(filename), "unknown")

    #####################################
    # try_transform tests

    @patch('server.src.uploads.file_transformation.FileTransformation.transform_image', return_value=True)
    def test_transform_does_not_saves_if_successful_transform(self, mock_transform_image):
        file_mock = Mock(spec=FileStorage)
        upload_path = 'test_files/transformation/output/test.jpg'

        FileTransformation.try_transform(file_mock, {"rotation": 90}, upload_path)

        file_mock.save.assert_not_called()
        mock_transform_image.assert_called_once()


    def test_transform_saves_if_no_transforms(self):
        file_mock = Mock(spec=FileStorage)
        upload_path = 'test_files/transformation/output/test.jpg'

        # Test with None
        FileTransformation.try_transform(file_mock, None, upload_path)

        file_mock.save.assert_called_once_with(upload_path)

    @patch('server.src.uploads.file_transformation.FileTransformation.transform_image', return_value=False)
    def test_transform_saves_if_no_valid_filetype(self, mock_transform_image):
        file_mock = Mock(spec=FileStorage)
        upload_path = 'some/path/file.txt'

        # Test with None
        FileTransformation.try_transform(file_mock, { "rotation": 90 }, upload_path)

        file_mock.save.assert_called_once_with(upload_path)
        mock_transform_image.assert_not_called()

    #######################
    # transform_image_tests
