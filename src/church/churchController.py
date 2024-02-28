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
from .churchModel import Church, ChurchSchema
from ..member.memberModel import Role
from .churchDAO import ChurchDAO
from ..member.memberDAO import MemberDAO
from marshmallow import ValidationError
from .churchService import church_name_exist

church_bp = Blueprint("church", __name__, url_prefix="/church")

church_schema = ChurchSchema()
churchDAO = ChurchDAO()


@church_bp.get("/")
def get_churches():
    try:
        churches = ChurchDAO().find_all()
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
@protectedRoute
def register_church():
    try:
        data = church_schema.load(request.json)
        user = decode_token(session.get("token")).get("user")
        if church_name_exist(data["name"], churchDAO):
            raise ValidationError("Church name already exist!")
            
        created_church = Church.create_church(data, user.get("_id"))
        res = churchDAO.insert(created_church.to_dict())
        member = MemberDAO().insert(
            {"church_id": res["_id"], "user_id": user.get("_id"), "role": Role.ADMIN.value})
        return good_response(res)
    except ValidationError as e:
        print(e)
        return bad_response(e.messages)


@church_bp.get("/<id>")
def get_church(id: str):
    try:
        church = churchDAO.find_by_id(id)
        return good_response(church)
    except Exception as e:
        print(e)
        return server_error()
