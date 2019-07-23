from flask import render_template, session, redirect, url_for
from sqlalchemy import exc

from chatty import app, socketio
from chatty.db import db
from chatty.db.models import User
from chatty.services import authentication
from chatty.services.authorization import requires_auth


@app.route('/auth', defaults={'action': 'login'})
@app.route('/auth/<action>')
def auth(action):
    return authentication.authenticate(action)


@app.route('/login')
def login():
    if session.get('user'):
        return redirect(url_for('.auth', action='logout', _external=True))
    return render_template('login.html')


@app.route('/')
@requires_auth
def index():
    user = User(session['user']['given_name'], session['user']['family_name'], session['user']['email'])
    db.session.add(user)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
    return render_template('index.html')


def messageRecived():
    print 'message was received!!!'


@socketio.on('my event')
def handle_my_custom_event(json):
    print 'recived my event: ' + str(json)
    socketio.emit('my response', json, callback=messageRecived)


if __name__ == '__main__':
    socketio.run(app, debug=True)
