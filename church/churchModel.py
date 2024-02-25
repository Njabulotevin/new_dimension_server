import datetime
from user.userModel import User
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
    def __init__(self, _id: str, role : Role) -> None:
        self._id = _id
        self.role = role
    
    def to_dict(self):
        return {
            "_id": self._id,
            "role": self.role.value
        }
    @classmethod
    def create_member(cls, member, role):
        member = Member(_id=member["_id"], role=role)
        return member.to_dict()

class Address:
    def __init__(self, street, city, province, country, postal_code):
        self.street = street
        self.city = city
        self.province = province
        self.country = country
        self.postal_code = postal_code

    def to_dict(self):
        return {
            "street": self.street,
            "city": self.city,
            "state": self.province,
            "country": self.country,
            "postal_code": self.postal_code
        }


class Contact:
    def __init__(self, phone, email, website):
        self.phone = phone
        self.email = email
        self.website = website

    def to_dict(self):
        return {
            "phone": self.phone,
            "email": self.email,
            "website": self.website
        }

class Service:
    def __init__(self, day, time):
        self.day = day
        self.time = time

    def to_dict(self):
        return {
            "day": self.day,
            "time": self.time
        }


class Church():
    def __init__(self, name ,denomination, address : Address, contact : Contact, services : Service, about, image_url, members : list[Member], followers_count=0, created_at=None, modified_at=None, creator=None):
        self.name = name
        self.denomination = denomination
        self.address = address
        self.contact = contact
        self.services = services
        self.about = about
        self.image_url = image_url
        self.members = members
        self.creator = creator
        self.followers_count = followers_count
        self.created_at = created_at if created_at else datetime.datetime.now()
        self.modified_at = modified_at if modified_at else datetime.datetime.now()

    def to_dict(self):
       return {
            "name": self.name,
            "denomination": self.denomination,
            "address": self.address,
            "contact": self.contact,
            "services": [service for service in self.services],
            "about": self.about,
            "image_url": self.image_url,
            "members": [member for member in self.members],
            "followers_count": self.followers_count,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "creator" : self.creator
        }
    
    @classmethod
    def create_church(self, church, creator):
        church = Church(name = church["name"], 
        denomination=church["denomination"], 
        address=church["address"],
        contact = dict(church["contact"]),
        services = list(church["services"]),
        about = church["about"],
        image_url=church["image_url"],
        members=[],
        followers_count=0, creator=creator)
        return church


    @classmethod
    def serialize_church(cls, church):
         return {
            "_id": str(church["_id"]),
            "name": church["name"],
            "denomination": church["denomination"],
            "address": dict(church["address"]),
            "contact": dict(church["contact"]),
            "services": list(church["services"]),
            "about": church["about"],
            "image_url": church["image_url"],
            "members": church["members"],
            "followers_count": church["followers_count"],
            "created_at": church["created_at"],
            "modified_at": church["modified_at"],
            "creator" : church["creator"]
        }

    @classmethod
    def serialize_churches(cls, churches):
        '''
        Serialize list of church documents from MongoDB
        '''
        return [cls.serialize_church(church) for church in churches] 


        
