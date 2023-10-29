from flask import Flask, jsonify
from auth.auth_views import auth_blueprint
from decouple import config
from flask_session import Session


app = Flask(__name__)
app.register_blueprint(auth_blueprint)

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['DEBUG'] = config('DEBUG', default=False)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
api_key = config('API_KEY')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def hello_world():
    return jsonify({"hello" : "world"})




if __name__ == "__main__":
    app.run(debug=True)