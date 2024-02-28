from flask import Blueprint, request, session
from utils.response import (
    bad_response,
    good_response,
    server_error,
    not_found,
    unauthorized,
)
from utils.token import decode_token
from middlewares.auth import protectedRoute
from .memberDAO import MemberDAO
from ..user.userDAO import UserDAO
from ..church.churchDAO import ChurchDAO
from .memberService import is_admin_member, find_member_by_church
from ..user.userService import get_user_id
from .memberModel import MemberSchema, MemberRoleSchema
from marshmallow import ValidationError


member_bp = Blueprint("member", __name__, url_prefix="/members")

churchDAO = ChurchDAO()
memberDAO = MemberDAO()
userDAO = UserDAO()

memberSchema = MemberSchema()
memberRoleSchema = MemberRoleSchema()

@member_bp.get("/<church_id>")
def get_church_members(church_id: str):
    try:
        church = churchDAO.find_by_id(church_id)

        if not church:
            return bad_response("Invalid church Id")

        members = memberDAO.find_by_church(church_id)
        return good_response(members)

    except Exception as e:
        print(e)
        return server_error()


@member_bp.route("/", methods=["POST"])
@protectedRoute
def add_members():
    try:
        data = memberSchema.load(request.json)
        member, church_id = data["user_id"], data["church_id"]
        user = get_user_id()
        church_exit = churchDAO.find_by_id(church_id)
        user_exist = userDAO.find_by_id(member)
        
        if not is_admin_member(user, church_id, memberDAO):
            return unauthorized()

        elif not church_exit:
            return bad_response("Invalid church Id")

        elif not user_exist:
            return bad_response("Invalid User Id")

        elif find_member_by_church(member, church_id, memberDAO):
            return bad_response("User already a member!")
        else:
            mapped_member = {"church_id": church_id,
                             "user_id": member, "role": "member"}
            added_member = memberDAO.insert(mapped_member)
            return good_response(added_member)

    except Exception as e:
        print(e)
        if isinstance(e, ValidationError):
            return bad_response(e.messages)
        return server_error()


@member_bp.route("/", methods=["PATCH"])
@protectedRoute
def change_member_role():
    try:
        data = memberRoleSchema.load(request.json)
        church_id, member_id, role = data["church_id"], data["user_id"], data["role"]
        user_id = get_user_id()
        member = find_member_by_church(member_id, church_id, memberDAO)
    
        if not is_admin_member(user_id, church_id, memberDAO):
            return unauthorized()
        if not member:
            return bad_response("Member not found!")
        else:
            if member["role"] != role.value:
                modified = memberDAO.update_member_role(member["_id"], role.value)    
                if modified > 0:
                    return good_response("Member role changed to " + str(role.value))
            return bad_response("Member role not modified!")
    except Exception as e:
        print(e)
        if isinstance(e, ValidationError):
            return bad_response(e.messages)
        return server_error()
