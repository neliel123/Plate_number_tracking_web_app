#This bluepint will deal with all user management functionality 

from flask import Blueprint

about_blueprint = Blueprint('about', __name__, template_folder='templates')

from . import views