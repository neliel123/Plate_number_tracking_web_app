import os
from flask import Flask, render_template
from flask_mail import Mail
from celery import Celery
from config import Config
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
from app.extensions import db, socketio, migrate, lm
from flask_login import LoginManager
from app.models import User  # Import your User model
from flask_login import LoginManager

# Flask extension objects instantiation
mail = Mail()

# Instantiate Celery
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, result_backend=Config.RESULT_BACKEND)

# Application Factory
def create_app():
    app = Flask(__name__)

    # Configure the flask app instance
    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)

    # Configure celery
    celery.conf.update(app.config)

    # Register blueprints
    register_blueprints(app)

    # Initialize flask extension objects
    initialize_extensions(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app

# Helper Functions
def register_blueprints(app):
    from app.auth import auth_blueprint
    from app.main import main_blueprint
    from app.api import api_blueprint
    from app.students import students_blueprint
    from app.motorcycles import motorcycles_blueprint
    from app.tracking import vehicle_tracking_blueprint
    from app.about import about_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(students_blueprint, url_prefix='/students')
    app.register_blueprint(motorcycles_blueprint, url_prefix='/motorycles')
    app.register_blueprint(vehicle_tracking_blueprint, url_prefix='/tracking')
    app.register_blueprint(about_blueprint, url_prefix='/about')

def initialize_extensions(app):
    mail.init_app(app)
    db.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)
    lm.init_app(app)

def register_error_handlers(app):

    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

def configure_logging(app):
    # Deactivate the default flask logger so that log messages don't get duplicated
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler('flaskapp.log', maxBytes=16384, backupCount=20)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)
