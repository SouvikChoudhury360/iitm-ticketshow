from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    isAdmin = db.Column(db.Boolean)
    name = db.Column(db.String(100))

class venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    address = db.Column(db.String(500))

class show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    ticket_price = db.Column(db.Integer)
    tags = db.Column(db.String(100))
    starting_time = db.Column(db.DateTime)
    ending_time = db.Column(db.DateTime)
    capacity = db.Column(db.Integer)
    venue_id = db.Column(db.Integer)

class bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    show_id = db.Column(db.Integer)
    count = db.Column(db.Integer)

class ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    show_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
