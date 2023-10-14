import os
from flask_cors import CORS

from app import create_app

if __name__ == '__main__':
    app = create_app()

    origins = os.environ.get("ORIGINS", "http://localhost:63342,http://localhost:63343").split(",")
    CORS(app, origins=origins)
    # CORS(app, origins=["http://localhost:63342"])
    app.run(debug=True, port=5001)