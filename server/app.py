from flask import Flask, request, send_from_directory, make_response
from flask_cors import CORS

from uploads.file_utility import FileUtility
from uploads.file_info_obfuscated_handler import FileInfoObfuscatedHandler
from uploads.file_manager import FileManager

app = Flask(__name__)

UPLOAD_FOLDER = FileUtility.ROOT
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    try:
        resource_name, upload_path = FileInfoObfuscatedHandler.get_upload_info(file, app.config["UPLOAD_FOLDER"])
        FileManager.upload_file(file, upload_path)
    except Exception as e:
        return 'Failed uploading', 500

    response = make_response({
        "url": f"view/{resource_name}"
    })
    response.headers["Content-Type"] = "application/json"
    return response, 200


@app.route('/v/<year>/<month>/<prefix>/<key>/<filename>', methods=['GET'])
def serve_file(year: str, month: str, prefix: str, key: str, filename: str) -> None:
    path = FileInfoObfuscatedHandler.get_filepath_from_uri(filename, app.config["UPLOAD_FOLDER"])
    return send_from_directory(path, filename, as_attachment=False)


@app.route('/d/<year>/<month>/<prefix>/<key>/<filename>', methods=['GET'])
def download_file(year: str, month: str, prefix: str, key: str, filename: str) -> None:
    path = FileInfoObfuscatedHandler.get_filepath_from_uri(filename, app.config["UPLOAD_FOLDER"])
    return send_from_directory(path, filename, as_attachment=True)


if __name__ == '__main__':
    CORS(app.run(debug=True, port=5001), origins=["http://localhost:63342"])
