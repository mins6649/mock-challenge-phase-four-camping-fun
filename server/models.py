from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship('Signup', backref = 'camper', cascade='all, delete, delete-orphan')

    serialize_rules = ('-signups.camper', '-created_at', '-updated_at')
    activities = association_proxy('signups', 'activity')

    @validates('name')
    def validates_name(self, key, value):
        if not value:
            raise ValueError("Please enter a name")
        return value
    @validates('age')
    def validates_age(self, key, value):
        if value < 8:
            raise ValueError("Too young")
        elif value > 18:
            raise ValueError("Too old")
        return value
    

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship('Signup', backref = 'activity', cascade='all, delete, delete-orphan')

    serialize_rules = ('-signups.activity','-created_at', '-updated_at')
    camper = association_proxy('signups', 'camper')


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    serialize_rules = ('-camper.signups', '-activity.signups', '-created_at', '-updated_at')

    @validates('time')
    def validates_time(self, key, value):
        if value < 0:
            raise ValueError("please select a viable time for activity")
        elif value > 23:
            raise ValueError("please select a viable time for activity")
        return value


