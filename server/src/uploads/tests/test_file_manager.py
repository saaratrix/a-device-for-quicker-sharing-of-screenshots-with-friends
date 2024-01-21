import os
import unittest
import shutil
import pytest
from typing import Tuple, IO

from ..file_manager import FileManager
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
            FileManager.upload_file(None, upload_path)


    def test_upload_file_throws_if_file_exists(self):
        file_name = 'test.txt'
        upload_path = os.path.join(self.test_folder, file_name)
        self.create_test_file(file_name)

        with pytest.raises(FileExistsError):
            FileManager.upload_file(None, upload_path)

    def test_upload_file_should_upload(self):
        mock_file_name = "mock.png"
        mock_path = os.path.join(self.test_folder, mock_file_name)
        handle, mock_file = self.create_mock_upload_file(mock_file_name)

        try:
            target_path = os.path.join(self.test_folder, 'upload.txt')

            assert os.path.exists(mock_path)
            assert not os.path.exists(target_path)

            FileManager.upload_file(mock_file, target_path)
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


if __name__ == '__main__':
    unittest.main()
