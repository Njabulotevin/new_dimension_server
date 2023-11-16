from flask_sqlalchemy import SQLAlchemy
from run import db

class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.string(255))

    def __repr__(self):
        return '<User %r>' % self.username