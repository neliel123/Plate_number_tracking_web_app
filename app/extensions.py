from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
socketio = SocketIO(app=None)
migrate = Migrate()  # Initialize Flask-Migrate
lm = LoginManager()