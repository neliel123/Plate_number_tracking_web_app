#This bluepint will deal with all user management functionality 

from flask import Blueprint

vehicle_tracking_blueprint = Blueprint('tracking', __name__, template_folder='templates')

from . import views