from flask import Flask, render_template
from src.user.userController import user_bp
from src.church.churchController import church_bp
from src.member.memberController import member_bp
from decouple import config
from flask_session import Session
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

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
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # with app.app_context():
    app.run(debug=True)
