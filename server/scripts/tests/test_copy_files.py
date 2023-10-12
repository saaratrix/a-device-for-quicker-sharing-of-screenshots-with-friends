import os
import shutil
import unittest

import pytest

from ..copy_files import copy_file, can_copy_file


class MoveFilesTests(unittest.TestCase):
    test_folder: str = ""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        file_directory = os.path.dirname(os.path.abspath(__file__))
        self.test_folder = os.path.join(file_directory, "test_files", "temp_test_files", "")
        yield
        pass
        if os.path.exists(self.test_folder):
            shutil.rmtree(self.test_folder)

    def test_copy_file_cool_file_copied(self) -> None:
        current_file = os.path.dirname(os.path.abspath(__file__))
        source_path = os.path.join(current_file, "test_files", "a_cool_file.txt")
        target_path = os.path.join(self.test_folder, "a_cool_file.txt")
        copy_file(source_path, target_path)
        os.path.exists(target_path)

    def test_can_copy_file_can_copy(self) -> None:
        test_data = [
            ["uploads/__init__.py", ["tests"]],
            ["uploads/file_info_handler.py", ["tests"]],
            ["uploads/file_utility.py", ["tests"]],
        ]

        for path, excludes in test_data:
            with self.subTest(path=path, excludes=excludes):
                can_copy = can_copy_file(path, excludes)
                assert can_copy

    def test_can_copy_file_cant_copy(self) -> None:
        test_data = [
            # Can't copy tests
            ["uploads/tests/__init__.py", ["tests"]],
            ["uploads/tests/test_file_manager.py", ["tests"]],
            ["uploads/test_file_utility.py", ["test"]],
        ]

        for path, excludes in test_data:
            with self.subTest(path=path, excludes=excludes):
                can_copy = can_copy_file(path, excludes)
                assert not can_copy


if __name__ == '__main__':
    unittest.main()
