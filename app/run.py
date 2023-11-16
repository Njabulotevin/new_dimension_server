from flask import Flask, jsonify
from auth.auth_views import auth_blueprint
from decouple import config
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from models.admin import Admin

app = Flask(__name__)
app.register_blueprint(auth_blueprint)

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['DEBUG'] = config('DEBUG', default=False)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
api_key = config('API_KEY')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

username = 'root'
password = 'test%401234'
database = 'new_dimensiondb'

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@localhost:5432/{database}"
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# class Admin(db.Model):
#     __tablename__ = 'Admin'
    
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255))
#     username = db.Column(db.String(255))
#     password = db.Column(db.string(255))

#     def __repr__(self):
#         return '<User %r>' % self.username


@app.route("/")
def hello_world():
    # res = Admin.query.all()
    return jsonify({"hello" : "world"})


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all() # <--- create db object.
    app.run(debug=True)