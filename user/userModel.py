import uuid


class User():
    def __init__(self, _id : str, created_at: int, modified_at: int, email : str, password : str) -> None:
        self._id = _id
        self.created_at = created_at
        self.modified_at = modified_at
        self.email = email
        self.password = password

    @classmethod
    def serialize_user_db(self, user):
        return {"_id": str(user["_id"]), "modified_at": None, "email": user["email"], "password" : user["password"]}

    @classmethod
    def serialize_users_db(cls, users: list) -> list:
        '''
        Serialize list of mongodb users
        '''
        return [cls.serialize_user_db(user) for user in users] 

    