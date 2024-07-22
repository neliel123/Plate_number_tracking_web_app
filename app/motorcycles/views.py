from . import motorcycles_blueprint
from flask import render_template, request, flash, redirect, url_for, current_app
from app.models import Motorcycle, Student
from app.extensions import db
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload
from flask_login import login_required

@motorcycles_blueprint.route("/")
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    motorcycles = Motorcycle.query.paginate(page=page, per_page=10)
    return render_template('list_motorcycles.html', motorcycles=motorcycles)

@motorcycles_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add_motorcycle():
    if request.method == "POST":
        plate_number = request.form['plate_number']
        model = request.form['model']
        owner_id = request.form['owner_id']

        new_motorcycle = Motorcycle(plate_number=plate_number, model=model, owner_id=owner_id)
        db.session.add(new_motorcycle)
        db.session.commit()
        flash("Motorcycle added successfully!", "success")
        return redirect(url_for('motorcycles.index'))

    students = Student.query.all()
    return render_template("add_motorcycle.html", students=students)

@motorcycles_blueprint.route("/edit/<int:motorcycle_id>", methods=["GET", "POST"])
@login_required
def edit_motorcycle(motorcycle_id):
    motorcycle = Motorcycle.query.get_or_404(motorcycle_id)

    if request.method == "POST":
        motorcycle.plate_number = request.form['plate_number']
        motorcycle.model = request.form['model']
        motorcycle.owner_id = request.form['owner_id']
        
        db.session.commit()
        flash("Motorcycle updated successfully!", "success")
        return redirect(url_for('motorcycles.index'))

    students = Student.query.all()
    return render_template("edit_motorcycle.html", motorcycle=motorcycle, students=students)

@motorcycles_blueprint.route("/delete/<int:motorcycle_id>", methods=["POST"])
@login_required
def delete_motorcycle(motorcycle_id):
    motorcycle = Motorcycle.query.get_or_404(motorcycle_id)
    db.session.delete(motorcycle)
    db.session.commit()
    flash("Motorcycle deleted successfully!", "success")
    return redirect(url_for('motorcycles.index'))

@motorcycles_blueprint.route("/search")
@login_required
def search():
    last_name = request.args.get('last_name', '', type=str)
    plate_number = request.args.get('plate_number', '', type=str)
    page = request.args.get('page', 1, type=int)
    
    query = Motorcycle.query.join(Student).options(joinedload(Motorcycle.owner))

    if last_name:
        query = query.filter(Student.last_name.ilike(f'%{last_name}%'))
    if plate_number:
        query = query.filter(Motorcycle.plate_number.ilike(f'%{plate_number}%'))

    motorcycles = query.paginate(page=page, per_page=10)
    return render_template('list_motorcycles.html', motorcycles=motorcycles)

@motorcycles_blueprint.route("/view/<int:motorcycle_id>")
@login_required
def view_motorcycle(motorcycle_id):
    motorcycle = Motorcycle.query.get_or_404(motorcycle_id)
    return render_template("view_motorcycle.html", motorcycle=motorcycle)
