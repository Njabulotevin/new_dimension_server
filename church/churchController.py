from flask import Blueprint, request, session
from utils.response import (
    bad_response,
    good_response,
    server_error,
    not_found,
    unauthorized,
)
from utils.token import decode_token
from middlewares.auth import protectedMiddleware
from church.churchModel import Church
from member.memberModel import Role
from database.database import ChurchDB, MemberDB
from bson import ObjectId

church_bp = Blueprint("church", __name__, url_prefix="/church")


@church_bp.get("/")
def get_churches():
    try:
        churches = ChurchDB().find_all()
        filter_churces = [
            {
                "_id": church["_id"],
                "name": church["name"],
                "image_url": church["image_url"],
            }
            for church in churches
        ]
        return good_response(filter_churces)
    except Exception as e:
        print(e)
        return server_error()


@church_bp.post("/register")
@protectedMiddleware
def register_church():
    try:
        data = request.get_json()
        user = decode_token(session.get("token")).get("user")
        created_church = Church.create_church(data, user.get("_id"))
        # created_church.members = [Member.create_member(user, Role.ADMIN)]
        res = ChurchDB().insert(created_church.to_dict())
        member = MemberDB().insert(
            {"church_id": res["_id"], "user_id": user.get("_id"), "role": Role.ADMIN.value})
        return good_response(res)
    except Exception as e:
        print(e)
        return server_error()


@church_bp.get("/<id>")
def get_church(id: str):
    try:
        church = ChurchDB().find_by_id(id)
        return good_response(church)
    except Exception as e:
        print(e)
        return server_error()
