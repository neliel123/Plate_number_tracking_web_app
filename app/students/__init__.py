#This bluepint will deal with all user management functionality 

from flask import Blueprint

students_blueprint = Blueprint('students', __name__, template_folder='templates')

from . import views