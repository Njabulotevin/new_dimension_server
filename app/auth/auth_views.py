from flask import Blueprint, request, session
from utils.response import bad_response, good_response, server_error, not_found, unauthorized
from decouple import config
from utils.token import gen_token
from middlewares.auth import protectedMiddleware
from database.db_conn import get_db_connection
import bcrypt
import uuid




auth_blueprint = Blueprint("admin", __name__, url_prefix='/admin')

@auth_blueprint.get("/<id>")
# @protectedMiddleware
def get_admin(id : str):
    try:
        user =  get_user(id)
        if user:
            user.pop("password")
            return good_response(user)
        return not_found("User not found!")
    except Exception as e:
        return server_error()


@auth_blueprint.post("/login")
def login():
    try:
        data = request.get_json()
        email, password = data["email"], data["password"]

        user = is_valid_user(email, password)
      
        if user:
            token = gen_token(user)
            session["token"] = token
            return good_response({"user": user})
        return bad_response("Invalid email or password")
    except Exception as e:
        if isinstance(e, KeyError):
            return bad_response(f"The following fields are missing: {e}")
        print(e)
        return "Server error", 500

@auth_blueprint.post("/register")
def register():
    try:
        data = request.get_json()
        email, username, password = data["email"], data["username"], data["password"]
        password = password.encode("utf8")
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password, salt)
        conn = get_db_connection()
        results = conn.execute("INSERT INTO admin (id, username, email, password) VALUES (?, ?, ?, ?)",
            (str(uuid.uuid4()), username, email, hashed_pw.decode("utf8")))
        conn.commit()
        conn.close()
        print(results)
        user = get_user(email=email)
        user.pop("password")
        return good_response({"user": user})
    except Exception as e:
        if "UNIQUE constraint failed: admin.email" in str(e):
            return bad_response("User already exist!")
        return server_error()


def is_valid_user(email : str, password : str):
    try:
        user = get_user(email=email)
        password_correct = bcrypt.checkpw(password.encode("utf8"), user["password"].encode("utf8"))
        if user:
            if email == user["email"] and password_correct:
                user.pop("password")
                return user
    except Exception as e:
        print(e)
        user = get_user(email=email)
        print(user)
        return False


def get_user(id = None, email = None) -> dict:
    try:
        conn = get_db_connection()
        users = conn.execute("SELECT * FROM admin").fetchall()
        conn.close()
        for user in users:
            if user["id"] == id or user["email"] == email:
                return {"email": user["email"], "username": user["username"], "id": user["id"], "password" : user["password"]}
    except:
        return None