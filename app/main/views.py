from . import main_blueprint
from flask import render_template, request, redirect, url_for, current_app, abort
from flask_login import login_required

@main_blueprint.route('/')
@login_required
def index():
    current_app.logger.info("Index page loading")
    return render_template('main/index.html')

@main_blueprint.route('/admin')
@login_required
def admin():
    abort(500)