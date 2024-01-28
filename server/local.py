import os
from flask_cors import CORS
from src.app import create_app

if __name__ == '__main__':
    # Asking ChatGPT for username & password makes it ninja themed, ok!
    os.environ['ADMIN_USERNAME'] = 'ninja'
    os.environ['ADMIN_PASSWORD'] = 'kuno'

    uploads_path = os.path.join(os.path.dirname(__file__), "file_uploads")
    app = create_app(uploads_path)

    origins = os.environ.get("ORIGINS", "http://localhost:63342,http://localhost:63343,http://localhost:63344,http://localhost:63345").split(",")
    CORS(app, origins=origins)
    # CORS(src, origins=["http://localhost:63342"])
    app.run(debug=True, port=5001)