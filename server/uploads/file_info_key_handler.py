import datetime
import hashlib
import os
import random
from typing import TYPE_CHECKING

from .file_utility import FileUtility

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage


class FileInfoKeyHandler:
    @staticmethod
    def get_upload_path(file: 'FileStorage', user_key: str, root: str = FileUtility.ROOT) -> str:
        now = datetime.datetime.now()
        time = now.time()
        hash_key = FileInfoKeyHandler.generate_hash(time)
        date_folder = FileInfoKeyHandler.get_date_folder_name(now)
        user_key = FileInfoKeyHandler.adjustUserKey(user_key)
        filename = f"{hash_key}_{file.filename}"
        return os.path.join(root, date_folder, user_key, filename)

    @staticmethod
    def get_filepath_from_request(year: str, month: str, prefix: str, key: str, filename: str, root: str = FileUtility.ROOT):
        filename = f"{prefix}_{filename}"
        return os.path.join(root, year, month, key, filename)

    @staticmethod
    def get_date_folder_name(date: datetime) -> str:
        date_formatted = date.strftime("%y%m")
        return os.path.join(date_formatted[:2], date_formatted[2:4])

    @staticmethod
    def generate_hash(time: float) -> str:
        # Get the current timestamp
        timestamp = str(time)

        # Create an MD5 hash of the timestamp
        result = hashlib.md5(timestamp.encode())

        # Get the hexadecimal representation of the hash
        hex_result = result.hexdigest()

        # Take the first 6 characters
        short_hash = hex_result[:6]
        return short_hash

    @staticmethod
    def adjustUserKey(userKey: str, desired_length: int = 10, min_length: int = 5) -> str:
        """
        Adjust the userKey to a desired length by adding random characters.
        If the userKey is shorter than min_length, random characters are added until min_length is reached.
        If the userKey is longer than desired_length, it's truncated.

        Parameters:
        - userKey: The input string.
        - desired_length: The desired length of the output string.
        - min_length: The minimum length before random characters are added.

        Returns:
        Adjusted userKey.
        """

        if len(userKey) < min_length:
            userKey += ''.join(random.choice(str.ascii_letters) for _ in range(min_length - len(userKey)))

        if len(userKey) > desired_length:
            userKey = userKey[:desired_length]

        return userKey