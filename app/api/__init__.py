#This bluepint will deal with all user management functionality 

from flask import Blueprint

api_blueprint = Blueprint('api', __name__, template_folder='templates')

from . import views