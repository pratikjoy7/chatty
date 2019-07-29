from flask import url_for, redirect, flash, session, request
from requests_oauthlib import OAuth2Session

from chatty.config import Config
from chatty.db import db
from chatty.db.models import User


def authenticate(action):
    if session.get('user'):
        if action in ['logout', 'revoke']:
            del session['user']
            return redirect(url_for('.login', _external=True))
        return redirect(url_for('.index', _external=True))

    google = OAuth2Session(Config.GOOGLE_CLIENT_ID, scope=['openid',
                                                           'https://www.googleapis.com/auth/userinfo.email',
                                                           'https://www.googleapis.com/auth/userinfo.profile'],
                           redirect_uri=url_for('.auth', _external=True), state=session.get('state'))

    if not request.args.get('state'):
        auth_url, state = google.authorization_url('https://accounts.google.com/o/oauth2/auth', access_type='offline')
        session['state'] = state
        return redirect(auth_url)

    if request.args.get('error'):
        error = request.args['error']
        if error == 'access_denied':
            error = 'Not logged in'
        flash('Error: {}'.format(error), 'danger')
        return redirect(url_for('.login'))

    google.fetch_token('https://accounts.google.com/o/oauth2/token', client_secret=Config.GOOGLE_CLIENT_SECRET,
                       authorization_response=request.url)

    user = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()

    session['user'] = user

    exists = db.session.query(User.id).filter_by(email=user['email']).scalar()

    if not exists:        
        return redirect(url_for('.welcome', _external=True))
    return redirect(url_for('.index', _external=True))
