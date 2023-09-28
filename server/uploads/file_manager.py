import os.path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage


class FileManager:

    @staticmethod
    def upload_file(file: 'FileStorage', upload_path: str):
        if os.path.exists(upload_path):
            raise Exception(f"File already exists {upload_path}")

        FileManager.ensure_directory_exists(upload_path)
        file.save(upload_path)

    @staticmethod
    def delete_file(path: str) -> bool:
        if not os.path.exists(path):
            return False
        os.remove(path)
        return True

    @staticmethod
    def delete_month(year: str, month: str, root: str):
        pass

    @staticmethod
    def ensure_directory_exists(file_path: str) -> None:
        """
        Ensure that the directory for the given file path exists.
        If it doesn't, create the necessary directories.
        """
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory, True)
