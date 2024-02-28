from database.database import MemberDB
from member.memberModel import Member


def find_user_by_church(user_id: str, church_id, memberDB: MemberDB):
    try:
        member = memberDB.find_by_query(
            {"user_id": user_id, "church_id": church_id})
        return member
    except Exception as e:
        print(e)
        return None


def is_admin_member(user_id: str, church_id, memberDB: MemberDB):
    member = find_user_by_church(user_id, church_id, memberDB)
    if member:
        return True
    return False
