from flask import Flask
from flask_cors import CORS
from database.connection import init_db
from routes.api_routes import api

app = Flask(__name__)

# Izinkan frontend Netlify mengakses semua endpoint backend
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(api)


@app.route("/")
def index():
    return {
        "message": "UStayEase Python Flask Backend is running",
        "api": "/api/health"
    }


init_db()


if __name__ == "__main__":
    app.run(debug=True)