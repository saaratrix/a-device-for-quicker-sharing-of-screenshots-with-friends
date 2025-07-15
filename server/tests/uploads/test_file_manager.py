import os
import unittest
import shutil
import pytest
from typing import Tuple, IO

from server.src.uploads.file_manager import FileManager
from werkzeug.datastructures import FileStorage


class TestFileManager(unittest.TestCase):
    test_folder: str = ""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        file_directory = os.path.dirname(os.path.abspath(__file__))
        self.test_folder = os.path.join(file_directory, "temp_test_files", "")
        yield
        pass
        if os.path.exists(self.test_folder):
            shutil.rmtree(self.test_folder)

    def create_test_file(self, name: str) -> None:
        FileManager.ensure_directory_exists(self.test_folder)
        path = os.path.join(self.test_folder, name)
        with open(path, 'w') as file:
            pass

    def create_mock_upload_file(self, name: str) -> Tuple[IO[bytes], 'FileStorage']:
        path = os.path.join(self.test_folder, name)
        self.create_test_file(name)
        f = open(path, 'rb')
        return f, FileStorage(f, filename=name)

    def test_upload_file_throws_if_blocked_filetype(self):
        file_name = '.htaccess'
        upload_path = os.path.join(self.test_folder, file_name)

        with self.assertRaises(ValueError):
            FileManager.upload_file(None, upload_path, None)

    def test_upload_file_throws_if_file_exists(self):
        file_name = 'test.txt'
        upload_path = os.path.join(self.test_folder, file_name)
        self.create_test_file(file_name)

        with pytest.raises(FileExistsError):
            FileManager.upload_file(None, upload_path, None)

    def test_upload_file_should_upload(self):
        mock_file_name = "mock.png"
        mock_path = os.path.join(self.test_folder, mock_file_name)
        handle, mock_file = self.create_mock_upload_file(mock_file_name)

        try:
            target_path = os.path.join(self.test_folder, 'upload.txt')

            assert os.path.exists(mock_path)
            assert not os.path.exists(target_path)

            FileManager.upload_file(mock_file, target_path, None)
            handle.close()
            assert os.path.exists(target_path)
        except:
            handle.close()
            pytest.fail("not supposed to throw.")

    def test_upload_file_should_upload_and_transform_image(self):
        mock_file_name = "mock.png"
        mock_path = os.path.join(self.test_folder, mock_file_name)
        handle, mock_file = self.create_mock_upload_file(mock_file_name)

        try:
            target_path = os.path.join(self.test_folder, 'upload.txt')

            assert os.path.exists(mock_path)
            assert not os.path.exists(target_path)

            FileManager.upload_file(mock_file, target_path, { "rotation": 90 })
            handle.close()
            assert os.path.exists(target_path)
        except:
            handle.close()
            pytest.fail("not supposed to throw.")

    def test_delete_existing_file(self):
        file_name = 'test.txt'
        self.create_test_file(file_name)
        file_path = os.path.join(self.test_folder, file_name)

        assert os.path.exists(file_path)

        assert FileManager.delete_file(file_path)
        assert not os.path.exists(file_path)

    def test_delete_nonexistent_file(self):
        file_name = 'nonexistent.txt'
        file_path = os.path.join(self.test_folder, file_name)

        assert not FileManager.delete_file(file_path)

    def create_test_directory_structure(self):
        os.makedirs(os.path.join(self.test_folder, "23", "01", "01"), exist_ok=True)

    def test_delete_date_existing_directory_recursively(self):
        self.create_test_directory_structure()
        directory_path = os.path.join(self.test_folder, "23")
        # Verify directories exist
        self.assertTrue(os.path.exists(directory_path))
        self.assertTrue(os.path.exists(os.path.join(directory_path, "01", "01")))

        self.assertTrue(FileManager.delete_date_directory_recursively(directory_path))
        # And then they don't
        self.assertFalse(os.path.exists(directory_path))

    def test_delete_date_nonexistent_directory(self):
        directory_path = os.path.join(self.test_folder, "nonexistent_directory")

        self.assertFalse(os.path.exists(directory_path))
        self.assertFalse(FileManager.delete_date_directory_recursively(directory_path))

    def test_delete_date_directory_with_incorrect_format(self):
        # Create a directory with a name that is not two digits
        os.makedirs(os.path.join(self.test_folder, "a"), exist_ok=True)
        directory_path = os.path.join(self.test_folder, "a")

        self.assertTrue(os.path.exists(directory_path))
        self.assertFalse(FileManager.delete_date_directory_recursively(directory_path))
        # Directory should still exist
        self.assertTrue(os.path.exists(directory_path))


if __name__ == '__main__':
    unittest.main()
