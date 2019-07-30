from sqlalchemy import exc

from chatty.db import db
from chatty.db.models import User


def create_user(user):
    user = User(user['given_name'], user['family_name'], user['email'], user['picture'])
    db.session.add(user)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session().rollback()


def update_public_key(email, public_key):
    user = User.query.filter_by(email=email).first()
    user.public_key = public_key
    db.session.commit()


def get_users_to_chat_with(email):
    return User.query.filter(User.email != email).all()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
