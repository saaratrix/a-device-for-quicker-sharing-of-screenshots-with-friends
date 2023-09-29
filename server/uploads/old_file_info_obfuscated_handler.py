import datetime
import glob
import os
import random
import string
from typing import Tuple, TYPE_CHECKING

from .file_utility import FileUtility

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage


class OldFileInfoObfuscatedHandler:
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

    @staticmethod
    def get_upload_info(file: 'FileStorage', root: str) -> Tuple[str, str]:
        """
        Get the upload path information so, we can store the file correctly.
        :param file: The uploaded file
        :param root: The root upload folder path.
        :return: Resource name without extension and full upload path.
        """
        now = datetime.datetime.now()
        folder_path, resource_name = OldFileInfoObfuscatedHandler.get_file_infos(now)
        extension = FileUtility.get_file_extension(file.filename)
        upload_path = os.path.join(root, folder_path, resource_name + extension)

        return resource_name, upload_path

    def get_filepath_from_uri(uri: str, root: str) -> str:
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

        date_decoded = date_encoded.translate(OldFileInfoObfuscatedHandler._DATE_CIPHER_REVERSE)
        folder_path = OldFileInfoObfuscatedHandler.get_folder_name(date_decoded)
        path = os.path.join(root, folder_path, uri)
        extension = OldFileInfoObfuscatedHandler.find_file_extension(path)
        return f"{path}{extension}"

    @staticmethod
    def find_file_extension(file_path) -> str:
        path = os.path.normpath(file_path)
        # Get the list of files in the specified directory
        files = glob.glob(path + ".*")

        # If there are matching files, return the first one found
        if files:
            return FileUtility.get_file_extension(files[0])
        else:
            return ""



    @staticmethod
    def get_file_infos(date: datetime.datetime, random_chars=None) -> Tuple[str, str]:
        """
        Get the folder path and resource name from input date.
        """

        if random_chars is None:
            random_chars = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))

        date_formatted = date.strftime("%y%m%d")
        datetime_formatted = date.strftime('%H%M%S')
        date_encoded = OldFileInfoObfuscatedHandler.get_encoded_date(date_formatted)
        timestamp_encoded = OldFileInfoObfuscatedHandler.get_encoded_name(datetime_formatted)
        resource_name = f"{random_chars[0]}{date_encoded}{random_chars[1]}{timestamp_encoded}{random_chars[2]}"
        folder_path = OldFileInfoObfuscatedHandler.get_folder_name(date_formatted)
        return folder_path, resource_name

    @staticmethod
    def get_folder_name(date: str) -> str:
        return os.path.join(date[:2], date[2:4], date[4:])

    @staticmethod
    def get_encoded_date(date: str) -> str:
        return date.translate(OldFileInfoObfuscatedHandler._DATE_CIPHER)

    @staticmethod
    def get_encoded_name(value: str) -> str:
        return value.translate(OldFileInfoObfuscatedHandler._NAME_CIPHER)

