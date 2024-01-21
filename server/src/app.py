from flask import Flask

from .routes.admin_stats import admin_stats
from .uploads.file_utility import FileUtility
from .routes.file_sharing_routes import file_sharing_bp


def create_app():
    app = Flask(__name__)
    UPLOAD_FOLDER = FileUtility.ROOT
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # bytes * kb * mb * gb, so 1 GB is current maximum size.
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 * 1

    app.register_blueprint(file_sharing_bp)
    app.register_blueprint(admin_stats)
    return app
