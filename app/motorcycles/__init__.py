#This bluepint will deal with all user management functionality 

from flask import Blueprint

motorcycles_blueprint = Blueprint('motorcycles', __name__, template_folder='templates')

from . import views