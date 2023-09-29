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
def get_allowed_extensions():
    return jsonify(
        extensions=FileUtility.ALLOWED_EXTENSIONS,
        maxlength_file=FileValidation.MAXLENGTH_FILENAME,
        maxlength_user=FileValidation.MAXLENGTH_USER_KEY
    )


@app.route('/upload', methods=['PUT'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    sanitized_filename = file.strip()
    try:
        FileUtility.validate_path(
            sanitized_filename,
            FileValidation.MAXLENGTH_FILENAME,
            FileValidation.ALLOW_EMPTY_DEFAULT,
        )
        FileUtility.validate_path(
            request.key,
            FileValidation.MAXLENGTH_USER_KEY,
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
            request.key,
            app.config["UPLOAD_FOLDER"]
        )
        FileManager.upload_file(file, upload_path)
    except Exception as e:
        return 'Failed uploading', 500

    response = make_response({
        "url": f"v/{uri_path}"
    })
    response.headers["Content-Type"] = "application/json"
    return response, 200


# View with & without key.
@app.route('/v/<year>/<month>/<day>/<prefix>/<key>/<filename>', methods=['GET'])
@app.route('/v/<year>/<month>/<day>/<prefix>/<filename>/', methods=['GET'], defaults={'key': None})
def serve_file(year: str, month: str, day: str, prefix: str, key: str, filename: str) -> None:
    try:
        path = get_file_path(year, month, day, prefix, key, filename)
    except:
        return "Invalid uri.", 400
    return send_from_directory(path, filename, as_attachment=False)


# Downloads with & without key
@app.route('/d/<year>/<month>/<day>/<prefix>/<key>/<filename>', methods=['GET'])
@app.route('/d/<year>/<month>/<day>/<prefix>/<filename>/', methods=['GET'], defaults={'key': None})
def download_file(year: str, month: str, day: str, prefix: str, key: str, filename: str) -> None:
    try:
        path = get_file_path(year, month, day, prefix, key, filename)
    except:
        return "Invalid uri.", 400

    return send_from_directory(path, filename, as_attachment=True)


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return "File size exceeds the allowed limit.", 413


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
    CORS(app.run(debug=True, port=5001), origins=["http://localhost:63342"])
