import os
import sys

# Get the path of the directory the wsgi.py file is in
current_path = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory
parent_path = os.path.dirname(current_path)
# Add the parent directory to sys.path
sys.path.append(parent_path)

from src.app import create_app

uploads_path = os.path.join(os.path.dirname(__file__), "file_uploads")
app = create_app(uploads_path, True)
