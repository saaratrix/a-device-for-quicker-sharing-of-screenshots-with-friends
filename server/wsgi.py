import os

from src.app import create_app

uploads_path = os.path.join(os.path.dirname(__file__), "file_uploads")
app = create_app(uploads_path)
