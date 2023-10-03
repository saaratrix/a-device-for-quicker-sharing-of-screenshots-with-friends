import os
import pathlib
import re


class FileValidation:
    MAXLENGTH_FILENAME = 42
    MAXLENGTH_DATE = 2
    # HASH_LENGTH + HASH_RANDOM_LENGTH
    MAXLENGTH_HASH = 8 + 8
    MAXLENGTH_USER_SECRET = MAXLENGTH_HASH

    ALLOW_EMPTY_DEFAULT = False
    ALLOW_EMPTY_USER_SECRET = True


class FileUtility:
    ROOT = "file_uploads"

    @staticmethod
    def get_file_extension(path: str) -> str:
        try:
            return pathlib.Path(path).suffix
        except Exception:
            return ''

    @staticmethod
    def validate_path(path, max_length, allow_empty):
        if not allow_empty and path == "":
            raise ValueError("Path is empty.")

        FileUtility.validate_path_length(path, max_length)
        FileUtility.validate_illegal_chars(path)

    @staticmethod
    def validate_path_length(path, max_length):
        # Check if path exceeds max length
        if len(path) > max_length:
            raise ValueError(f"Path length exceeds maximum allowed length. {path}")

    @staticmethod
    def validate_illegal_chars(path: str):
        if path.isspace():
            raise ValueError("Path is only whitespace.")

        # A list of the characters
        # illegal_chars = ['..', '/', '\\', '\0', ':', ';', '*', '?', '"', '<', '>', '|']
        illegal_pattern = re.compile(r'(\.\.|[/\\:\0;*?"<>|])')
        match = illegal_pattern.search(path)

        if match:
            raise ValueError(f"Invalid characters found. {path}")

    ALLOWED_EXTENSIONS = [
        # Images
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp',
        # Videos
        '.mp4', '.mkv', '.flv', '.webm', '.mov', '.avi', '.m4v',
        # Audio
        '.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a',
        # Archives
        '.zip', '.rar', '.tar', '.gz', '.7z', '.tar.gz',
        # Documents
        '.txt', '.rtf', '.pdf', '.doc', '.docx', '.odt', '.ppt', '.pptx', '.xls', '.xlsx',
        # 3D Models
        '.obj', '.fbx', '.dae', '.3ds', '.blend', '.ply', '.stl',
        # Textures
        '.dds', '.ktx', '.pkm', '.tga',
        # WebFiles
        '.xml',
    ]

    @staticmethod
    def is_file_allowed(filename):
        # Extract the extension from the filename and check its presence in the ALLOWED_EXTENSIONS set
        base, ext = os.path.splitext(filename)
        return bool(base) and ext.lower() in FileUtility.ALLOWED_EXTENSIONS
