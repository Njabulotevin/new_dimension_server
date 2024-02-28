from .memberDAO import MemberDAO


def find_user_by_church(user_id: str, church_id, MemberDAO: MemberDAO):
    try:
        member = MemberDAO.find_by_query(
            {"user_id": user_id, "church_id": church_id})
        return member
    except Exception as e:
        print(e)
        return None


def is_admin_member(user_id: str, church_id, MemberDAO: MemberDAO):
    member = find_user_by_church(user_id, church_id, MemberDAO)
    if member:
        return True
    return False
