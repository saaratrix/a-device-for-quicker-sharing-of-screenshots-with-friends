import datetime
import glob
import os
import pathlib
import random
import string
from typing import Tuple


class FileHandler:
    _DATE_CIPHER = str.maketrans(
        '0123456789',
        '3ou57rg1wf'
    )
    _DATE_CIPHER_REVERSE = str.maketrans(
        '3ou57rg1wf',
        '0123456789'
    )

    _NAME_CIPHER = str.maketrans(
        '0123456789',
        '6v9c0r28s4'
    )

    ROOT = "file_uploads"

    @staticmethod
    def get_upload_info(file, root: str = ROOT) -> Tuple[str, str]:
        """
        Get the upload path information so, we can store the file correctly.
        :param file: The uploaded file
        :param root: The root upload folder path.
        :return: Resource name without extension and full upload path.
        """
        now = datetime.datetime.now()
        folder_path, resource_name = FileHandler.get_file_infos(now)
        extension = FileHandler.get_file_extension(file.filename)
        upload_path = os.path.join(root, folder_path, resource_name + extension)

        return resource_name, upload_path

    def get_filepath_from_uri(uri: str, root: str = ROOT) -> str:
        """
        Get the filepath from the uri.
        Uri format is in XDDDDDDXXXXXXXX.
        Where X = a random character
        D = date
        X = other characters.
        """
        if len(uri) != 15:
            raise ValueError("Invalid URI length")

        date_encoded = uri[1:7]

        date_decoded = date_encoded.translate(FileHandler._DATE_CIPHER_REVERSE)
        folder_path = FileHandler.get_folder_name(date_decoded)
        path = os.path.join(root, folder_path, uri)
        extension = FileHandler.find_file_extension(path)
        return f"{path}{extension}"

    @staticmethod
    def find_file_extension(file_path) -> str:
        path = os.path.normpath(file_path)
        # Get the list of files in the specified directory
        files = glob.glob(path + ".*")

        # If there are matching files, return the first one found
        if files:
            return FileHandler.get_file_extension(files[0])
        else:
            return ""

    @staticmethod
    def get_file_extension(path) -> str:
        try:
            return pathlib.Path(path).suffix
        except AttributeError:
            return ''

    @staticmethod
    def get_file_infos(date: datetime.datetime, random_chars=None) -> Tuple[str, str]:
        """
        Get the folder path and resource name from input date.
        """

        if random_chars is None:
            random_chars = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))

        date_formatted = date.strftime("%y%m%d")
        datetime_formatted = date.strftime('%H%M%S')
        date_encoded = FileHandler.get_encoded_date(date_formatted)
        timestamp_encoded = FileHandler.get_encoded_name(datetime_formatted)
        resource_name = f"{random_chars[0]}{date_encoded}{random_chars[1]}{timestamp_encoded}{random_chars[2]}"
        folder_path = FileHandler.get_folder_name(date_formatted)
        return folder_path, resource_name

    @staticmethod
    def get_folder_name(date: str) -> str:
        return os.path.join(date[:2], date[2:4], date[4:])

    @staticmethod
    def get_encoded_date(date: str) -> str:
        return date.translate(FileHandler._DATE_CIPHER)

    @staticmethod
    def get_encoded_name(value: str) -> str:
        return value.translate(FileHandler._NAME_CIPHER)


