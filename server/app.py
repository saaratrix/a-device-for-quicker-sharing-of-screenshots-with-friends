from flask import Flask, request, send_from_directory, make_response
from flask_cors import CORS

from uploads.file_utility import FileUtility
from uploads.file_info_handler import FileInfoHandler
from uploads.file_manager import FileManager

app = Flask(__name__)

UPLOAD_FOLDER = FileUtility.ROOT
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['PUT'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    sanitized_filename = FileUtility.sanitize_path(file.filename)
    if sanitized_filename == '':
        return 'No selected file', 400
    try:
        sanitized_key = FileUtility.sanitize_path(request.key)
        upload_path = FileInfoHandler.get_upload_path(
            sanitized_filename,
            sanitized_key,
            app.config["UPLOAD_FOLDER"]
        )
        FileManager.upload_file(file, upload_path)
    except Exception as e:
        return 'Failed uploading', 500

    response = make_response({
        "url": f"v/{resource_name}"
    })
    response.headers["Content-Type"] = "application/json"
    return response, 200


@app.route('/v/<year>/<month>/<day>/<prefix>/<key>/<filename>', methods=['GET'])
def serve_file(year: str, month: str, day: str, prefix: str, key: str, filename: str) -> None:
    path = get_file_path(year, month, day, prefix, key, filename)
    return send_from_directory(path, filename, as_attachment=False)


@app.route('/d/<year>/<month>/<day>/<prefix>/<key>/<filename>', methods=['GET'])
def download_file(year: str, month: str, day: str, prefix: str, key: str, filename: str) -> None:
    path = get_file_path(year, month, day, prefix, key, filename)
    return send_from_directory(path, filename, as_attachment=True)

def get_file_path(year: str, month: str, day: str, prefix: str, key: str, filename: str) -> str:
    sanitized_year = FileUtility.sanitize_path(year)
    sanitized_month = FileUtility.sanitize_path(month)
    sanitized_day = FileUtility.sanitize_path(day)
    sanitized_prefix = FileUtility.sanitize_path(prefix)
    sanitized_key = FileUtility.sanitize_path(key)
    sanitized_filename = FileUtility.sanitize_path(filename)

    return FileInfoHandler.get_filepath_from_request(
        sanitized_year,
        sanitized_month,
        sanitized_day,
        sanitized_prefix,
        sanitized_key,
        sanitized_filename,
        app.config["UPLOAD_FOLDER"]
    )


if __name__ == '__main__':
    CORS(app.run(debug=True, port=5001), origins=["http://localhost:63342"])
