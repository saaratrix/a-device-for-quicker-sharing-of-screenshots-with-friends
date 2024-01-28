import os.path

from flask import Flask

from .routes.file_sharing_routes import file_sharing_bp
from .routes.admin_stats import admin_stats_bp
from .routes.admin_delete import admin_delete_bp


def create_app(upload_folder='file_uploads'):
    app = Flask(__name__)
    UPLOAD_FOLDER = upload_folder
    if not (os.path.exists(UPLOAD_FOLDER)):
        raise NotADirectoryError(f"Directory not found {UPLOAD_FOLDER}")

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # bytes * kb * mb * gb, so 1 GB is current maximum size.
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 * 1

    app.register_blueprint(file_sharing_bp)
    app.register_blueprint(admin_stats_bp)
    app.register_blueprint(admin_delete_bp)
    return app
