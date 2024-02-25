from flask import Blueprint, request, session
from utils.response import bad_response, good_response, server_error, not_found, unauthorized
from utils.token import decode_token
from middlewares.auth import protectedMiddleware
from church.churchModel import Church, Member, Role
from database.database import ChurchDB




church_bp = Blueprint("church", __name__, url_prefix='/church')


@church_bp.get("/")
def get_churches():
    return good_response([])


@church_bp.post("/register")
@protectedMiddleware
def register_church():
    try:
        data = request.get_json()
        user= decode_token(session.get("token")).get("user")
        created_church = Church.create_church(data, user.get("_id"))
        created_church.members = [Member.create_member(user, Role.ADMIN)]
        res = ChurchDB().insert(created_church.to_dict())
        return good_response(res)
    except Exception as e:
        print(e)
        return server_error()