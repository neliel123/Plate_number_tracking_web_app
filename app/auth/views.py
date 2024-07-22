from . import auth_blueprint
from flask import render_template, request, redirect, url_for, flash
from ..tasks import send_celery_email
from app.extensions import lm
from app.models import User
from flask_login import login_user, logout_user, current_user
from app.util.decorators import logout_required
from flask_login import login_required

@auth_blueprint.route('/register/<string:email>')
def register(email):
    message_data={
        'subject': 'Hello from the flask app!',
        'body': 'This email was sent asynchronously using Celery.',
        'recipients': email,

    }
    send_celery_email.apply_async(args=[message_data])
    return render_template('auth/register.html', email=email)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')

    return render_template('login.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@lm.unauthorized_handler
def unauthorized():
    # Redirect unauthorized users to login page
    return redirect(url_for('auth.login'))