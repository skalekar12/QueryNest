from flask import Flask, send_from_directory
from flask_cors import CORS
from app.api.routes import router

app = Flask(__name__)
CORS(app)

app.register_blueprint(router, url_prefix="/api")

@app.get("/")
def frontend():
    return send_from_directory('..', 'index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)