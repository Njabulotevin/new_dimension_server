from database.database import DB_Collection
from bson import ObjectId
from .userModel import User


class UserDAO(DB_Collection):
    def __init__(self):
        super().__init__(collection_name="users")

    def insert(self, item):
        user_id = self.collection.insert_one(item).inserted_id
        user = self.collection.find_one({"_id": user_id})
        return User.serialize_user_db(user)

    def find_all(self):
        users = User.serialize_users_db(self.collection.find())
        return users

    def find_by_id(self, id: str):
        try:
            user = self.collection.find_one({"_id": ObjectId(id)})
            if user:
                return User.serialize_user_db(user)
            return None
        except Exception as e:
            print(e)
            return None

    def find_by_query(self, query):
        user = self.collection.find_one(query)
        return User.serialize_user_db(user)
