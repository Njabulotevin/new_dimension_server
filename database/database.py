from database.db_conn import get_database
from user.userModel import User
from church.churchModel import Church
from bson import ObjectId


class DB_Collection():
    def __init__(self, collection_name):
        connect_db = get_database()
        self.db = connect_db["new_dimension"]
        self.collection = self.db[collection_name]

class ChurchDB(DB_Collection):
    def __init__(self):
        super().__init__(collection_name="churches")

    def insert(self, church_data):
        # Validate church data
        if not all(key in church_data for key in ("name", "denomination", "address", "contact", "services", "creator")):
            raise ValueError("Required fields missing in church data.")

        # Ensure address, contact, and services are dictionaries
        if not isinstance(church_data["address"], dict) or not isinstance(church_data["contact"], dict) or not isinstance(church_data["services"], list):
            raise ValueError("Invalid data types for address, contact, or services.")

        # Ensure each service has required fields
        for service in church_data["services"]:
            if not all(key in service for key in ("day", "time")):
                raise ValueError("Each service must have 'day' and 'time' fields.")

        # Insert church data
        church_id = self.collection.insert_one(church_data).inserted_id
        return Church.serialize_church(self.find_by_id(church_id))

    def find_by_id(self, id):
        user = self.collection.find_one({"_id": ObjectId(id)})
        return Church.serialize_church(user)

class UserDB(DB_Collection):
    def __init__(self):
        super().__init__(collection_name="users")

    def insert(self, item):
        user_id = self.collection.insert_one(item).inserted_id
        user = self.collection.find_one({"_id":user_id})
        return User.serialize_user_db(user)

    def find_all(self):
        users = User.serialize_users_db(self.collection.find())
        return users
      
    def find_by_id(self, id : str):
        user = self.collection.find_one({"_id": ObjectId(id)})
        return User.serialize_user_db(user)

    def find_by_query(self, query):
        user = self.collection.find_one(query)
        return User.serialize_user_db(user)
       

def delete_item(id:str):
    pass


def update_item(id:str):
    pass