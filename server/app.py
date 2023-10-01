import os.path

from flask import Flask, request, send_from_directory, make_response, jsonify
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge

from uploads.file_utility import FileUtility, FileValidation
from uploads.file_info_handler import FileInfoHandler
from uploads.file_manager import FileManager

app = Flask(__name__)

UPLOAD_FOLDER = FileUtility.ROOT
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# bytes * kb * mb * gb, so 1 GB is current maximum size.
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 * 1


@app.route("/upload-info", methods=["GET"])
def get_upload_info():
    return jsonify(
        extensions=FileUtility.ALLOWED_EXTENSIONS,
        maxlengthFile=FileValidation.MAXLENGTH_FILENAME,
        maxlengthSecret=FileValidation.MAXLENGTH_SECRET_KEY
    )


@app.route('/upload', methods=['PUT'])
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
            request.form.get('key'),
            FileValidation.MAXLENGTH_SECRET_KEY,
            FileValidation.ALLOW_EMPTY_USER_KEY,
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
            request.form.get('key'),
            app.config["UPLOAD_FOLDER"]
        )
        FileManager.upload_file(file, upload_path)
    except Exception as e:
        return 'Failed uploading', 500

    return jsonify(
        url=f"v/{uri_path}"
    )


# View with & without key.
@app.route('/v/<year>/<month>/<day>/<prefix>/<key>/<filename>', methods=['GET'])
@app.route('/v/<year>/<month>/<day>/<prefix>/<filename>/', methods=['GET'], defaults={'key': None})
def view_file(year: str, month: str, day: str, prefix: str, key: str, filename: str) -> None:
    return send_file(year, month, day, prefix, key, filename, False)


# Downloads with & without key
@app.route('/d/<year>/<month>/<day>/<prefix>/<key>/<filename>', methods=['GET'])
@app.route('/d/<year>/<month>/<day>/<prefix>/<filename>/', methods=['GET'], defaults={'key': None})
def download_file(year: str, month: str, day: str, prefix: str, key: str, filename: str) -> None:
    return send_file(year, month, day, prefix, key, filename, True)


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return "File size exceeds the allowed limit.", 413


def send_file(year: str, month: str, day: str, prefix: str, key: str, filename: str, as_attachment):
    try:
        path, full_filename = get_file_path(year, month, day, prefix, key, filename)
        if not os.path.exists(path):
            raise FileExistsError("File not found.")
    except:
        return "Invalid uri.", 400

    return send_from_directory(path, full_filename, as_attachment=as_attachment)


def get_file_path(year: str, month: str, day: str, prefix: str, key: str, filename: str) -> str:
    try:
        FileUtility.validate_path(year, FileValidation.MAXLENGTH_DATE, FileValidation.ALLOW_EMPTY_DEFAULT)
        FileUtility.validate_path(month, FileValidation.MAXLENGTH_DATE, FileValidation.ALLOW_EMPTY_DEFAULT)
        FileUtility.validate_path(day, FileValidation.MAXLENGTH_DATE, FileValidation.ALLOW_EMPTY_DEFAULT)
        FileUtility.validate_path(prefix, FileValidation.MAXLENGTH_HASH, FileValidation.ALLOW_EMPTY_DEFAULT)
        FileUtility.validate_path(key, FileValidation.MAXLENGTH_HASH, FileValidation.ALLOW_EMPTY_USER_KEY)
        FileUtility.validate_path(filename, FileValidation.MAXLENGTH_FILENAME, FileValidation.ALLOW_EMPTY_DEFAULT)
    except ValueError as e:
        raise Exception(f"Invalid uri.")

    return FileInfoHandler.get_filepath_from_request(
        year,
        month,
        day,
        prefix,
        key,
        filename,
        app.config["UPLOAD_FOLDER"]
    )


if __name__ == '__main__':
    CORS(app, origins=["http://localhost:63342"])
    app.run(debug=True, port=5001)
