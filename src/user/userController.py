from flask import Blueprint, request, session
from utils.response import bad_response, good_response, server_error, not_found, unauthorized
# from decouple import config
from utils.token import gen_token
from middlewares.auth import protectedRoute
import bcrypt
import uuid
from .userService import is_valid_user, get_user
from .userDAO import UserDAO


user_bp = Blueprint("user", __name__, url_prefix='/user')


@user_bp.get("/<id>")
def get_user_controller(id: str):
    try:
        user = UserDAO().find_by_id(str(id))
        return good_response(user)
    except Exception as e:
        print(e)
        return server_error()


@user_bp.post("/login")
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


@user_bp.post("/register")
def register():
    try:
        data = request.get_json()
        email, username, password = data["email"], data["username"], data["password"]
        password = password.encode("utf8")
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password, salt)

        user = get_user(email=email)
        if user:
            return bad_response("User Already exist!")

        user = UserDAO().insert(
            {"email": email, "password": hashed_pw.decode("utf8")})
        user.pop("password")
        return good_response({"user": user})
    except Exception as e:
        print(e)
        if "UNIQUE constraint failed: user.email" in str(e):
            return bad_response("User already exist!")
        return server_error()
