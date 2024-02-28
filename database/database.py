from database.db_conn import get_database
from user.userModel import User
from member.memberModel import Member
from church.churchModel import Church
from bson import ObjectId
from enum import Enum


class UpdateOperation(Enum):
    PUSH = "$push"
    ADD_TO_SET = "$addToSet"
    PULL = "$pull"
    PULL_ALL = "$pullAll"
    POP = "$pop"
    INC = "$inc"
    MUL = "$mul"
    MIN = "$min"
    MAX = "$max"
    SET = "$set"
    UNSET = "$unset"


class DB_Collection:
    def __init__(self, collection_name):
        connect_db = get_database()
        self.db = connect_db["new_dimension"]
        self.collection = self.db[collection_name]


class ChurchDB(DB_Collection):
    def __init__(self):
        super().__init__(collection_name="churches")

    def insert(self, church_data):
        # Validate church data
        if not all(
            key in church_data
            for key in (
                "name",
                "denomination",
                "address",
                "contact",
                "services",
                "creator",
            )
        ):
            raise ValueError("Required fields missing in church data.")

        # Ensure address, contact, and services are dictionaries
        if (
            not isinstance(church_data["address"], dict)
            or not isinstance(church_data["contact"], dict)
            or not isinstance(church_data["services"], list)
        ):
            raise ValueError(
                "Invalid data types for address, contact, or services.")

        # Ensure each service has required fields
        for service in church_data["services"]:
            if not all(key in service for key in ("day", "time")):
                raise ValueError(
                    "Each service must have 'day' and 'time' fields.")

        # Insert church data
        church_id = self.collection.insert_one(church_data).inserted_id
        return Church.serialize_church(self.find_by_id(church_id))

    def find_by_id(self, id):
        try:
            church = self.collection.find_one({"_id": ObjectId(id)})
            if church:
                return Church.serialize_church(church)
            return None
        except Exception as e:
            print(e)
            return None

    def find_all(self):
        churches = self.collection.find()
        if churches:
            return Church.serialize_churches(churches)
        return None

    def update_one(self, filter_criteria, operation: UpdateOperation, key, data):
        try:
            update_data = {operation.value: {key: data}}
            self.collection.update_one(filter_criteria, update_data)
            return True
        except Exception as e:
            print(e)
            return False

    def update_list(self, filter_criteria, operation: UpdateOperation, key, data):
        try:
            update_data = {operation.value: {key:   data}}
            results = self.collection.update_one(filter_criteria, update_data)
            return results.modified_count
        except Exception as e:
            print(e)
            return 0


class MemberDB(DB_Collection):
    def __init__(self):
        super().__init__(collection_name="members")

    def find_by_id(self, id):
        try:
            member = self.collection.find_one({"_id": ObjectId(id)})
            if member:
                return Member.serialize_member(member)
            return None
        except Exception as e:
            print(e)
            return None

    def find_by_church(self, church_id):
        members = self.collection.find({"church_id": church_id})
        print("Church members found: ", members)
        if members:
            return Member.serialize_members(members)
        return None

    def find_by_user(self, user_id):
        member = self.collection.find_one({"user_id": user_id})
        if member:
            return Member.serialize_member(member)

        return None

    def insert(self, item):

        member_id = self.collection.update_one(
            {"user_id": item["user_id"]}, {"$set": item}, upsert=True)
        # member = self.collection.find_one({"_id": member_id})
        # return Member.serialize_member(member)
        return {}

    def insert_many(self, items):
        member_ids = self.collection.insert_many(items).inserted_ids
        members = []

        for member_id in member_ids:
            member = self.collection.find_one({"_id": member_id})
            members.append(member)

        return Member.serialize_members(members)

    def find_by_query(self, query):
        try:
            member = self.collection.find_one(query)
            return Member.serialize_member(member)
        except:
            return None


class UserDB(DB_Collection):
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


def delete_item(id: str):
    pass


def update_item(id: str):
    pass
