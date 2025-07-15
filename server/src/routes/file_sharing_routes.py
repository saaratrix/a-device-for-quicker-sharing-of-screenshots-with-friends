import os.path
import json
from typing import Dict, Optional
from flask import Blueprint, request, send_from_directory, jsonify, current_app, Response
from ..uploads.file_info_handler import FileInfoHandler
from ..uploads.file_manager import FileManager
from ..uploads.file_utility import FileUtility, FileValidation
from werkzeug.exceptions import RequestEntityTooLarge

file_sharing_bp = Blueprint('file_sharing_bp', __name__)


@file_sharing_bp.route("/upload-info", methods=["GET"])
def get_upload_info():
    return jsonify(
        extensions=FileUtility.ALLOWED_EXTENSIONS,
        maxlengthFile=FileValidation.MAXLENGTH_FILENAME,
        maxlengthSecret=FileValidation.MAXLENGTH_USER_SECRET
    )


@file_sharing_bp.route('/upload', methods=['PUT'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    sanitized_filename = request.form.get('filename').strip()
    try:
        FileUtility.validate_path(
            sanitized_filename,
            FileValidation.MAXLENGTH_FILENAME,
            FileValidation.ALLOW_EMPTY_DEFAULT,
        )
        FileUtility.validate_path(
            request.form.get('secret'),
            FileValidation.MAXLENGTH_USER_SECRET,
            FileValidation.ALLOW_EMPTY_USER_SECRET,
        )
    except:
        return f"Invalid file format.", 400

    if file.filename == '':
        return 'Invalid file format.', 400

    if not FileUtility.is_file_allowed(file.filename):
        return 'Invalid file format', 400

    try:
        uri_path, upload_path = FileInfoHandler.get_upload_path(
            sanitized_filename,
            request.form.get('secret'),
            current_app.config["UPLOAD_FOLDER"]
        )
        transform_actions = get_transform_actions(request.form.get('transformActions'))

        FileManager.upload_file(file, upload_path, transform_actions)
    except Exception as e:
        return 'Failed uploading', 500

    return jsonify(
        url=f"/v/{uri_path}"
    )


@file_sharing_bp.route('/v/<year>/<month>/<day>/<prefix>/<secret>/<filename>', methods=['GET'])
def view_file_with_secret(year: str, month: str, day: str, prefix: str, secret: str, filename: str) -> tuple[str, int] | Response:
    return send_file(year, month, day, prefix, secret, filename, False)


@file_sharing_bp.route('/v/<year>/<month>/<day>/<prefix>/<filename>', methods=['GET'])
def view_file_no_secret(year: str, month: str, day: str, prefix: str, filename: str) -> tuple[str, int] | Response:
    return send_file(year, month, day, prefix, "", filename, False)


@file_sharing_bp.route('/d/<year>/<month>/<day>/<prefix>/<secret>/<filename>', methods=['GET'])
def download_file_with_secret(year: str, month: str, day: str, prefix: str, secret: str, filename: str) -> tuple[str, int] | Response:
    return send_file(year, month, day, prefix, secret, filename, True)


@file_sharing_bp.route('/d/<year>/<month>/<day>/<prefix>/<filename>', methods=['GET'])
def download_file_no_secret(year: str, month: str, day: str, prefix: str, filename: str) -> tuple[str, int] | Response:
    return send_file(year, month, day, prefix, "", filename, True)


@file_sharing_bp.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return "File size exceeds the allowed limit.", 413


# Convert the upload edit settings eg: rotation, crop etc.
def get_transform_actions(transform_actions_json: Optional[str]) -> Dict | None:
    try:
        if transform_actions_json:
            return json.loads(transform_actions_json)
    except json.JSONDecodeError:
        pass
    return None


def send_file(year: str, month: str, day: str, prefix: str, user_secret: str, filename: str, as_attachment):
    try:
        path, full_filename = get_file_path(year, month, day, prefix, user_secret, filename)
        if not os.path.exists(path):
            raise FileExistsError("File not found.")
    except:
        return "Invalid uri.", 400

    return send_from_directory(path, full_filename, as_attachment=as_attachment)


def get_file_path(year: str, month: str, day: str, prefix: str, user_secret: str, filename: str) -> str:
    try:
        FileUtility.validate_path(year, FileValidation.MAXLENGTH_DATE, FileValidation.ALLOW_EMPTY_DEFAULT)
        FileUtility.validate_path(month, FileValidation.MAXLENGTH_DATE, FileValidation.ALLOW_EMPTY_DEFAULT)
        FileUtility.validate_path(day, FileValidation.MAXLENGTH_DATE, FileValidation.ALLOW_EMPTY_DEFAULT)
        FileUtility.validate_path(prefix, FileValidation.MAXLENGTH_HASH, FileValidation.ALLOW_EMPTY_DEFAULT)
        FileUtility.validate_path(user_secret, FileValidation.MAXLENGTH_HASH,
                                  FileValidation.ALLOW_EMPTY_USER_SECRET)
        FileUtility.validate_path(filename, FileValidation.MAXLENGTH_FILENAME, FileValidation.ALLOW_EMPTY_DEFAULT)
    except ValueError as e:
        raise Exception(f"Invalid uri.")

    return FileInfoHandler.get_filepath_from_request(
        year,
        month,
        day,
        prefix,
        user_secret,
        filename,
        current_app.config["UPLOAD_FOLDER"]
    )
