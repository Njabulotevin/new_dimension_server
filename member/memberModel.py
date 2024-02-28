from enum import Enum


class Role(Enum):
    ADMIN = 'admin'
    MEMBER = 'member'
    VISITOR = 'visitor'
    BISHOP = 'bishop'
    PASTOR = 'pastor'
    ELDER = 'elder'
    DEACON = 'deacon'
    OTHER_LEADER = 'other_leader'


class Member():
    def __init__(self, _id: str, church_id: str, user_id, role: Role) -> None:
        self._id = _id
        self.church_id = church_id
        self.user_id = user_id
        self.role = role

    def to_dict(self):
        return {
            "_id": self._id,
            "role": self.role.value
        }

    @classmethod
    def create_member(cls, member, role):
        member = Member(_id=member["_id"], role=role,
                        user_id=member["user_id"], church_id=member["church_id"])
        return member.to_dict()

    @classmethod
    def serialize_member(cls, member):
        return {
            "_id": str(member["_id"]),
            "church_id": member["church_id"],
            "user_id": member["user_id"],
            "role": member["role"]
        }

    @classmethod
    def serialize_members(cls, members):
        return [cls.serialize_member(member) for member in members]
