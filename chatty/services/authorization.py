from functools import wraps
from flask import session, redirect, url_for


def is_authorized():
    return session.get('user')


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authorized():
            return redirect(url_for('.login', _external=True))

        return f(*args, **kwargs)
    return decorated
