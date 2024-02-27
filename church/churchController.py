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
from church.churchModel import Church, Member, Role
from database.database import ChurchDB, UpdateOperation
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
        created_church.members = [Member.create_member(user, Role.ADMIN)]
        res = ChurchDB().insert(created_church.to_dict())
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


@church_bp.route("/members/<church_id>", methods=["POST"])
def add_members(church_id: str):
    try:
        data = request.get_json()
        members = data["members"]
        user = decode_token(session.get("token")).get("user").get("_id")

        if not isinstance(members, list) and not all(
            isinstance(id, str) for id in members
        ):
            return bad_response("Members must be a list of user Ids")
        else:
            mapped_members =  [{"_id": member, "role":"member"} for member in members]
            update = ChurchDB().update_list(
                {"_id": ObjectId(church_id)},
                UpdateOperation.PUSH,
                "members",
                mapped_members,
            )
            if update > 0:
                return good_response({"_id": church_id, "members": mapped_members})
            return bad_response("Could not update the members!")
    except Exception as e:
        print(e)
        return server_error()
