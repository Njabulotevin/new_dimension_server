from database.database import DB_Collection, UpdateOperation
from .churchModel import Church
from bson import ObjectId


class ChurchDAO(DB_Collection):
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

    def find_by_query(self, query):
        try:
            church = self.collection.find_one(query)
            return Church.serialize_church(church)
        except:
            return None