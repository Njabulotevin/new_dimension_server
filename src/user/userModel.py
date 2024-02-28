from marshmallow import Schema, fields, ValidationError

class User():
    def __init__(self, _id: str, created_at: int, modified_at: int, email: str, password: str) -> None:
        self._id = _id
        self.created_at = created_at
        self.modified_at = modified_at
        self.email = email
        self.password = password

    @classmethod
    def serialize_user_db(self, user):
        return {"_id": str(user["_id"]), "modified_at": None, "email": user["email"], "password": user["password"]}

    @classmethod
    def serialize_users_db(cls, users: list) -> list:
        '''
        Serialize list of mongodb users
        '''
        return [cls.serialize_user_db(user) for user in users]


class UserSchema(Schema):
    name = fields.Str(required=True)
    display_name= fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    confirm_password=fields.Str(required=True, load_only=True)
    
    # Custom validation method to check password equality
    def validate_confirm_password(self, data):
        if data['confirm_password'] != data['password']:
            raise ValidationError("Passwords do not match")

    # Call the custom validation method during deserialization
    @property
    def _declared_fields(self):
        return super()._declared_fields | {"confirm_password": self.fields["confirm_password"]}