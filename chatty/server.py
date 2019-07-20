import os

from flask import Flask, render_template, session, redirect, url_for
from flask_socketio import SocketIO, emit

from chatty.config import Config
from chatty.services import authentication
from chatty.services.authorization import requires_auth


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO( app )

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
  return render_template('index.html')


def messageRecived():
  print 'message was received!!!'


@socketio.on('my event')
def handle_my_custom_event(json):
  print 'recived my event: ' + str(json)
  socketio.emit('my response', json, callback=messageRecived)


if __name__ == '__main__':
  socketio.run(app, debug = True)
