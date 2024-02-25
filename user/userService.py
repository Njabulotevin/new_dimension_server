from utils.response import bad_response, good_response, server_error, not_found, unauthorized
from decouple import config
from utils.token import gen_token
from middlewares.auth import protectedMiddleware
import bcrypt
from database.database import UserDB




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
        return False


def get_user(id = None, email = None) -> dict:
    try:
        user= UserDB().find_by_query({"email": email})
        if user:
            return user
        return None
    except Exception as e:
        # print("From Alchemy: ", e)
        return None