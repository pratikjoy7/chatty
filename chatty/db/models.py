from chatty.db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(100))
    last_name = db.Column('last_name', db.String(100))
    email = db.Column('email', db.String(200), unique=True)
    avatar_url = db.Column('avatar_url', db.String(200))
    public_key = db.Column('public_key', db.String(500))

    def __init__(self, first_name, last_name, email, avatar_url, public_key):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.avatar_url = avatar_url
        self.public_key = public_key
