from . import about_blueprint
from flask import Blueprint, render_template

@about_blueprint.route('/')
def index():
    return render_template('about.html')