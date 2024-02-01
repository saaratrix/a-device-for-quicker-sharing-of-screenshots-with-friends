import os
import sys
import logging
# Append the parent path or `server.` doesn't work in child modules.
current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(current_path)
sys.path.append(parent_path)

from src.app import create_app

uploads_path = os.path.join(os.path.dirname(__file__), "file_uploads")
app = create_app(uploads_path, True)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
