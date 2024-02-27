from flask import session
from utils.token import is_valid_token
from utils.response import unauthorized


def protectedMiddleware(fn):
    def wrapper(*args, **kwargs):
        print("Is there a token? ", "token" in session)
        if "token" in session:
            token = session["token"]
            print("is valid token: ", is_valid_token(token))
            if not token or not is_valid_token(token):
                return unauthorized()
        else:
            return unauthorized()
        return fn(*args, **kwargs)
    return wrapper