import os

from flask import Flask
from chatty.config import Config
from flask_socketio import SocketIO

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)
