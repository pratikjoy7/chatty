from chatty.db import db
from chatty.db.models import UserSession
from chatty.services import user


def create_session(email, session_id):
    session_user = user.get_user_by_email(email)
    delete_session_ids_of_user(session_user)

    userSession = UserSession(session_id=session_id, user=session_user)
    db.session.add(userSession)
    db.session.commit()


def get_session_ids_of_user(email):
    session_user = user.get_user_by_email(email)
    session = UserSession.query.filter_by(user=session_user).first()

    return session.session_id


def delete_session_ids_of_user(user):
    UserSession.query.filter_by(user=user).delete()
    db.session.commit()
