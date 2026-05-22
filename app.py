from flask import Flask
from flask_cors import CORS
from config import Config
from database.connection import init_db
from routes.api_routes import api

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": Config.FRONTEND_URL if Config.FRONTEND_URL != "*" else "*"}})
app.register_blueprint(api)

@app.route("/")
def index():
    return {"message": "UStayEase Python Flask Backend is running", "api": "/api/health"}

init_db()

if __name__ == "__main__":
    app.run(debug=True)
