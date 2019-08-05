from flask import render_template, session, redirect, url_for, Response, request
from flask_socketio import SocketIO, emit

from chatty import app, socketio
from chatty.services import authentication, key_pair_generation, user, user_session
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


@app.route('/welcome')
def welcome():
    user.create_user(session['user'])
    return render_template('welcome.html')


@app.route('/private-key')
@requires_auth
def private_key():
    private_key = key_pair_generation.generate_key_pair()
    filename = '%s_chatty_private_key.pem' % session['user']['given_name']
    return Response(private_key,
                    mimetype="text/plain",
                    headers={"Content-Disposition":
                             "attachment;filename=%s" % filename})


@app.route('/')
@requires_auth
def index():
    users = user.get_users_to_chat_with(session['user']['email'])
    return render_template('index.html', users=users)


def messageRecived():
    print 'message was received!!!'


@socketio.on('user_session', namespace='/private')
def set_user_session(email):
    user_session.create_session(email, request.sid)


@socketio.on('message_sent', namespace='/private')
def process_message(payload):
    if payload.get('encrypt', ''):
        payload['message'] = user.encrypt_message(payload['recipient'], payload['message'])
    session_id = user_session.get_session_id_of_user(payload['recipient'])
    emit('new_private_message', payload, room=str(session_id))


@socketio.on('decrypt_message', namespace='/private')
def decrypt_message(payload):
    payload['message'] = user.decrypt_message(payload['message'], payload['private_key'])
    session_id = user_session.get_session_id_of_user(payload['email'])
    emit('new_decrypted_msg', payload, room=str(session_id))


if __name__ == '__main__':
    socketio.run(app, debug=True)
