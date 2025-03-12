from . import db
from flask_login import UserMixin
from datetime import datetime


class Candidate(db.Model):
    __bind_key__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    position = db.Column(db.String(200), nullable=False)
    votes = db.Column(db.Integer, default=0)
    deadline = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Candidate %r>' % self.name
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


