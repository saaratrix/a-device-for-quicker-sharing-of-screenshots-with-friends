import datetime
import hashlib
import os
import random
import secrets
import string
from typing import Tuple

class FileInfoHandler:
    HASH_LENGTH = 8
    HASH_RANDOM_LENGTH = 8

    @staticmethod
    def get_upload_path(original_filename: str, user_secret: str, root: str) -> str:
        now = datetime.datetime.now()
        time = now.time()
        hash_key = FileInfoHandler.generate_hash(time)
        date_formatted, date_folder = FileInfoHandler.get_date_folder_name(now)
        filename = f"{hash_key}_{original_filename}"

        uri_path = FileInfoHandler.get_uri_path(date_formatted, hash_key, user_secret, original_filename)
        upload_path = os.path.join(root, date_folder, user_secret, filename)
        return uri_path, upload_path

    @staticmethod
    def get_uri_path(date_formatted: str, prefix: str, user_secret: str, filename: str) -> str:
        uri_path = f"{date_formatted[:2]}/{date_formatted[2:4]}/{date_formatted[4:]}/{prefix}"
        if user_secret != "": uri_path += f"/{user_secret}"
        uri_path += f"/{filename}"
        return uri_path

    @staticmethod
    def get_filepath_from_request(year: str, month: str, day: str, prefix: str, user_secret: str, filename: str, root: str):
        filename = f"{prefix}_{filename}"
        path = os.path.join(root, year, month, day, user_secret)
        return path, filename

    @staticmethod
    def get_date_folder_name(date: datetime) -> Tuple[str, str]:
        date_formatted = date.strftime("%y%m%d")
        date_folder_name = os.path.join(date_formatted[:2], date_formatted[2:4], date_formatted[4:])
        return date_formatted, date_folder_name

    @staticmethod
    def generate_hash(time: float) -> str:
        timestamp = str(time)
        result = hashlib.sha1(timestamp.encode())
        hex_result = result.hexdigest()

        characters = string.ascii_letters + string.digits
        random_part = ''.join(secrets.choice(characters) for i in range(FileInfoHandler.HASH_RANDOM_LENGTH))
        hash_part = hex_result[:FileInfoHandler.HASH_LENGTH]

        # Interleave the hash and random characters
        combined_hash = ''.join(a + b for a, b in zip(hash_part, random_part))

        return combined_hash
