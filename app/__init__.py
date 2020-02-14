from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)

app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'flasknotewithsqlalchemy'
db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode = None)

from app import apis, models