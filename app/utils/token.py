from decouple import config
import datetime
import jwt



def gen_token(data):
    secret = config("SECRET_KEY")
    payload = {"user": data, "exp":  datetime.datetime.utcnow() + datetime.timedelta(hours=3)}
    return jwt.encode(payload, secret, algorithm="HS256")



def is_valid_token(token):
    secret = config("SECRET_KEY")
    try:
    # Verify and decode the JWT
        decoded_payload = jwt.decode(token, secret, algorithms=["HS256"])
    # The token is valid, and you can access its data in the `decoded_payload` dictionary.
        return True
    except jwt.ExpiredSignatureError:
        # Token has expired
        return "expired"
    except jwt.DecodeError:
        return "invalid"