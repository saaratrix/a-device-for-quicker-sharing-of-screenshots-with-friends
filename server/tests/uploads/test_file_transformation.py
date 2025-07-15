import os
import shutil
import unittest
from PIL import Image
from typing import Tuple, IO
from unittest.mock import Mock, patch

import pytest
from werkzeug.datastructures import FileStorage

from server.src.uploads.file_manager import FileManager
from server.src.uploads.file_transformation import FileTransformation


class TestFileTransformation(unittest.TestCase):
    test_input_folder: str = ""
    test_output_folder: str = ""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        file_directory = os.path.dirname(os.path.abspath(__file__))
        self.test_input_folder = os.path.join(file_directory, "test_files", "transformation", "")
        self.test_output_folder = os.path.join(self.test_input_folder, "output", "")
        yield
        pass
        if os.path.exists(self.test_output_folder):
            shutil.rmtree(self.test_output_folder)

    def create_test_file(self, name: str, copy_source: str | None) -> None:
        FileManager.ensure_directory_exists(self.test_output_folder)
        path = os.path.join(self.test_output_folder, name)
        if copy_source and os.path.exists(copy_source):
            with open(copy_source, 'rb') as src_file, open(path, 'wb') as dst_file:
                dst_file.write(src_file.read())
        else:
            # Just create an empty file if no source
            with open(path, 'wb') as file:
                pass

    def create_mock_upload_file(self, name: str, source: str | None) -> Tuple[IO[bytes], 'FileStorage']:
        path = os.path.join(self.test_output_folder, name)
        self.create_test_file(name, source)
        f = open(path, 'rb')
        return f, FileStorage(f, filename=name)

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
    def test_try_transform_does_not_saves_if_successful_transform(self, mock_transform_image):
        file_mock = Mock(spec=FileStorage)
        upload_path = 'test_files/transformation/output/test.jpg'

        FileTransformation.try_transform(file_mock, {"rotation": 90}, upload_path)

        file_mock.save.assert_not_called()
        mock_transform_image.assert_called_once()


    def test_try_transform_saves_if_no_transforms(self):
        file_mock = Mock(spec=FileStorage)
        upload_path = 'test_files/transformation/output/test.jpg'

        # Test with None
        FileTransformation.try_transform(file_mock, None, upload_path)

        file_mock.save.assert_called_once_with(upload_path)

    @patch('server.src.uploads.file_transformation.FileTransformation.transform_image', return_value=False)
    def test_try_transform_saves_if_no_valid_filetype(self, mock_transform_image):
        file_mock = Mock(spec=FileStorage)
        upload_path = 'some/path/file.txt'

        # Test with None
        FileTransformation.try_transform(file_mock, { "rotation": 90 }, upload_path)

        file_mock.save.assert_called_once_with(upload_path)
        mock_transform_image.assert_not_called()

    #######################
    # transform_image_tests
    def test_transform_image_does_nothing_if_no_valid_transformations(self):
        mock_file_name = "before.jpg"
        transformed_name = "after.jpg"
        mock_path = os.path.join(self.test_output_folder, mock_file_name)
        input_path = os.path.join(self.test_input_folder, "mymmis.jpg")
        handle, mock_file = self.create_mock_upload_file(mock_file_name, input_path)

        try:
            target_path = os.path.join(self.test_output_folder, transformed_name)

            assert os.path.exists(mock_path)
            assert not os.path.exists(target_path)

            FileTransformation.transform_image(mock_file, {}, target_path)
            handle.close()
            # should not save as no transformation was done.
            assert not os.path.exists(target_path)
        except:
            handle.close()
            pytest.fail("not supposed to throw.")

    def test_transform_image_should_rotate_image(self):
        mock_file_name = "before.jpg"
        transformed_name = "after.jpg"
        mock_path = os.path.join(self.test_output_folder, mock_file_name)
        input_path = os.path.join(self.test_input_folder, "mymmis.jpg")
        handle, mock_file = self.create_mock_upload_file(mock_file_name, input_path)

        before_dimensions = (128, 88)
        after_dimensions = (before_dimensions[1], before_dimensions[0])

        try:
            target_path = os.path.join(self.test_output_folder, transformed_name)

            assert os.path.exists(mock_path)
            assert not os.path.exists(target_path)

            FileTransformation.transform_image(mock_file, { "rotation": 90 }, target_path)
            handle.close()
            # should not save as no transformation was done.
            assert os.path.exists(target_path)

            with Image.open(mock_path) as before_img, Image.open(target_path) as after_img:
                before_size = before_img.size
                after_size = after_img.size

                assert before_size == (before_size[0], before_size[1]), "Starting image was expected dimensions"
                assert after_dimensions == (after_size[0], after_size[1]), f"Image should be rotated"

        except:
            handle.close()
            pytest.fail("not supposed to throw.")
