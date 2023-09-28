import pathlib


class FileUtility:
    ROOT = "file_uploads"

    @staticmethod
    def get_file_extension(path: str) -> str:
        try:
            return pathlib.Path(path).suffix
        except Exception:
            return ''

    @staticmethod
    def sanitize_path(path):
        sanitized = path.replace("..", "").replace("/", "").replace("\\", "")
        return sanitized