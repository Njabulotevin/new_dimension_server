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
from database.database import MemberDB, ChurchDB, UserDB
from member.memberService import is_admin_member, find_user_by_church


member_bp = Blueprint("member", __name__, url_prefix="/members")

churchDB = ChurchDB()
memberDB = MemberDB()
userDB = UserDB()


@member_bp.get("/<church_id>")
def get_church_members(church_id: str):
    try:
        church = churchDB.find_by_id(church_id)

        if not church:
            return bad_response("Invalid church Id")

        members = memberDB.find_by_church(church_id)
        return good_response(members)

    except Exception as e:
        print(e)
        return server_error()


@member_bp.route("/<church_id>", methods=["POST"])
@protectedMiddleware
def add_members(church_id: str):
    try:
        data = request.get_json()
        member = data["member"]
        user = decode_token(session.get("token")).get("user").get("_id")
        church_exit = churchDB.find_by_id(church_id)
        user_exist = userDB.find_by_id(member)

        if not is_admin_member(user, church_id, memberDB):
            return unauthorized()

        if not isinstance(member, str):
            return bad_response("Member must be an Id")

        elif not church_exit:
            return bad_response("Invalid church Id")

        elif not user_exist:
            return bad_response("Invalid User Id")

        elif find_user_by_church(member, church_id, memberDB):
            return bad_response("User already a member!")
        else:
            mapped_member = {"church_id": church_id,
                             "user_id": member, "role": "member"}
            added_member = memberDB.insert(mapped_member)
            return good_response(added_member)

    except Exception as e:
        print(e)
        return server_error()
