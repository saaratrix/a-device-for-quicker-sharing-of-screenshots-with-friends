import os.path
import shutil
from typing import TYPE_CHECKING

from .file_transformation import FileTransformationOptions, FileTransformation
from .file_utility import FileUtility

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage


class FileManager:
    @staticmethod
    def upload_file(file: 'FileStorage', upload_path: str, transform_actions: FileTransformationOptions):
        if not FileUtility.is_file_allowed(upload_path):
            raise ValueError(f"Fileformat is not allowed. {upload_path}")

        if os.path.exists(upload_path):
            raise FileExistsError(f"File already exists {upload_path}")

        FileManager.ensure_directory_exists(upload_path)
        FileTransformation.try_transform(file, transform_actions, upload_path)

    @staticmethod
    def try_delete_file(path: str) -> bool:
        if not os.path.exists(path):
            return False
        os.remove(path)
        return True

    @staticmethod
    def delete_file(folder: str, filename: str) -> bool:
        full_path = os.path.join(folder, filename)
        return FileManager.try_delete_file(full_path)

    @staticmethod
    def delete_date_directory_recursively(path: str) -> bool:
        if not os.path.exists(path) or not os.path.isdir(path):
            return False
        last_component = os.path.basename(path.rstrip(os.sep))

        # If for some reason the directory isn't 2 digits then we do nothing.
        if not (len(last_component) == 2 and last_component.isdigit()):
            return False

        shutil.rmtree(path)
        return True

    @staticmethod
    def ensure_directory_exists(file_path: str) -> None:
        """
        Ensure that the directory for the given file path exists.
        If it doesn't, create the necessary directories.
        """
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory, 0o777, True)
