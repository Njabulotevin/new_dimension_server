from flask import session
from utils.token import is_valid_token
from utils.response import unauthorized


def protectedMiddleware(fn):
    def wrapper(*args, **kwargs):
        if "token" in session:
            token = session["token"]
            if not token or not is_valid_token(token):
                return unauthorized()
        else:
            return unauthorized()
        return fn(*args, **kwargs)
    return wrapper