from flask import Blueprint, request, session
from utils.response import bad_request, good_request, server_error, not_found, unauthorized
from decouple import config
from utils.token import gen_token
from middlewares.auth import protectedMiddleware




auth_blueprint = Blueprint("admin", __name__, url_prefix='/admin')


dummy_users = [
        {
            "id": "a1c28c6b-e932-4423-958a-9ea427e69d0b",
            "username": "user1",
            "email": "user1@example.com",
            "password": "password1"
        },
        {
            "id": "24e7f7a2-72a2-48ab-8776-1f0f3ec4f09b",
            "username": "user2",
            "email": "user2@example.com",
            "password": "password2"
        },
        {
            "id": "c7a301f8-9ca5-4813-920c-798b5e0e3301",
            "username": "user3",
            "email": "user3@example.com",
            "password": "password3"
        },
        {
            "id": "5a9f344a-1a84-43d7-95df-7c6b6e4ddce5",
            "username": "user4",
            "email": "user4@example.com",
            "password": "password4"
        },
        {
            "id": "b9f999f6-8937-48b7-9b8e-0b16dd53c073",
            "username": "user5",
            "email": "user5@example.com",
            "password": "password5"
        }
    ]




@auth_blueprint.get("/<id>")
@protectedMiddleware
def get_admin(id : str):
    try:
        user =  get_user(id)
        if user:
            return good_request(user)
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
            return good_request({"user": user})
        return bad_request("Invalid email or password")
    except Exception as e:
        if isinstance(e, KeyError):
            return bad_request(f"The following fields are missing: {e}")
        print(e)
        return "Server error", 500

@auth_blueprint.post("/register")
def register():
    try:
        data = request.get_json()
        email, username, password = data["email"], data["username"], data["password"]
        # admin = Admin(email=email, username=username, password=password, id=1)
        # db.session.add(admin)
        # db.session.commit()
        return "Registered!"
    except Exception as e:
        print(e)
        return server_error()


def is_valid_user(email : str, password : str):
    user = get_user(email=email)
    if user:
         if email == user["email"] and password == user["password"]:
            return user
    return False


def get_user(id = None, email = None) -> dict:
    try:
        for user in dummy_users:
            if user["id"] == id or user["email"] == email:
                return user
    except:
        return None