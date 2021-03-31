from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    tasks = db.relationship('Task',
        backref=db.backref('user', lazy=True))

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_url = db.Column(db.String(100))
    is_booked = db.Column(db.Boolean)
    tasks = db.relationship('Task',
        backref=db.backref('dataset', lazy=True))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'),
        nullable=False)
    is_onwork = db.Column(db.Boolean)
    is_booked = db.Column(db.Boolean)