from . import students_blueprint
from flask import render_template, request, jsonify, render_template, flash, redirect, url_for, current_app
from app.models import Student
from app.extensions import db
from werkzeug.utils import secure_filename
import os
import uuid
from flask_login import login_required

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@students_blueprint.route("/")
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    first_name = request.args.get('first_name', '', type=str)
    last_name = request.args.get('last_name', '', type=str)
    
    query = Student.query
    if first_name:
        query = query.filter(Student.first_name.ilike(f'%{first_name}%'))
    if last_name:
        query = query.filter(Student.last_name.ilike(f'%{last_name}%'))
        
    students = query.paginate(page=page, per_page=10)
    
    return render_template('list_students.html', students=students, first_name=first_name, last_name=last_name)


@students_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "POST":
        tup_id = request.form['tup_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        section = request.form['section']
        picture = request.files['picture']

        # Validate the picture file
        if picture and allowed_file(picture.filename):
            if request.content_length > MAX_CONTENT_LENGTH:
                flash("File size exceeds the 2MB limit.", "danger")
                return redirect(request.url)
            filename = secure_filename(picture.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"

            # Ensure the upload directory exists
            upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)

            picture_path = os.path.join(upload_path, unique_filename)
            picture.save(picture_path)
            picture_url = os.path.join(UPLOAD_FOLDER, unique_filename).replace("\\", "/")
        else:
            flash("Invalid file type. Only png, jpg, jpeg, and gif files are allowed.", "danger")
            return redirect(request.url)

        new_student = Student(tup_id=tup_id, first_name=first_name, last_name=last_name, email=email, section=section, picture_path=picture_url)
        db.session.add(new_student)
        db.session.commit()
        flash("Student added successfully!", "success")
        return redirect(url_for('students.index'))

    return render_template("add_student.html")




@students_blueprint.route("/view/<int:student_id>")
@login_required
def view_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template("view_student.html", student=student)

@students_blueprint.route('/<int:id>', methods=['GET'])
@login_required
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.as_dict()), 200

@students_blueprint.route('/', methods=['POST'])
@login_required
def create_student():
    data = request.get_json()
    new_student = Student(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        picture_path=data.get('picture_path')
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.as_dict()), 201

@students_blueprint.route('/<int:id>', methods=['PUT'])
@login_required
def update_student(id):
    data = request.get_json()
    student = Student.query.get_or_404(id)
    student.first_name = data.get('first_name', student.first_name)
    student.last_name = data.get('last_name', student.last_name)
    student.email = data.get('email', student.email)
    student.picture_path = data.get('picture_path', student.picture_path)
    db.session.commit()
    return jsonify(student.as_dict()), 200

@students_blueprint.route("/edit/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == "POST":
        student.tup_id = request.form['tup_id']
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.email = request.form['email']
        student.section = request.form['section']
        picture = request.files['picture']
        student.section = request.form['section']

        # Validate and save the new picture if uploaded
        if picture and allowed_file(picture.filename):
            if request.content_length > MAX_CONTENT_LENGTH:
                flash("File size exceeds the 2MB limit.", "danger")
                return redirect(request.url)
            
            filename = secure_filename(picture.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"

            # Ensure the upload directory exists
            upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)

            picture_path = os.path.join(upload_path, unique_filename)
            picture.save(picture_path)
            new_picture_path = os.path.join(UPLOAD_FOLDER, unique_filename).replace("\\", "/")

            # Delete the old picture if it exists
            if student.picture_path:
                old_picture_path = os.path.join(current_app.root_path, student.picture_path)
                print(f"old_picture_path :: {old_picture_path}")
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)
            
            student.picture_path = new_picture_path

        db.session.commit()
        flash("Student updated successfully!", "success")
        return redirect(url_for('students.index'))

    return render_template("edit_student.html", student=student)

@students_blueprint.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted'}), 200

# Add this method to the Student model to easily convert to dictionary
def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

Student.as_dict = as_dict