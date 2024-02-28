from database.database import DB_Collection
from .memberModel import Member
from bson import ObjectId


class MemberDAO(DB_Collection):
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

    def insert_set(self, item):
        member_id = self.collection.insert_one(
            {"user_id": item["user_id"]}, {"$set": item}, upsert=True)
        return {}

    def insert(self, item):
        try:
            member_id = self.collection.insert_one(item).inserted_id
            member = self.collection.find_one({"_id": member_id})
            return Member.serialize_member(member)
        except Exception as e:
            print(e)
            return None

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
    
    def update_member_role(self, member_id ,new_role : str):
        try:
            member = self.collection.update_one({"_id": ObjectId(member_id)}, {"$set": {"role" : new_role}})
            return member.modified_count
        except Exception as e:
            print(e)
            return 0
