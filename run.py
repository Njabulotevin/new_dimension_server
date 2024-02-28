from flask import Flask, jsonify
from user.userController import user_bp
from church.churchController import church_bp
from member.memberController import member_bp
from decouple import config
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
# from models.admin import Admin
import uuid
from database.db_conn import get_database
from user.userModel import User

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(user_bp)
app.register_blueprint(church_bp)
app.register_blueprint(member_bp)

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['DEBUG'] = config('DEBUG', default=False)
app.config['DATABASE_URI'] = config('DATABASE_URL')
api_key = config('API_KEY')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_COOKIE_DOMAIN'] = 'localhost:3000'
app.config["SESSION_FILE_DIR"] = "./flask_session_cache"
Session(app)


@app.route("/")
def hello_world():
    return jsonify({"hello": "world"})


if __name__ == "__main__":
    # with app.app_context():
    app.run(debug=True)
