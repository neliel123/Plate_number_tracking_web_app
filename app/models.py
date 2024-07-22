from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from app.extensions import db
from flask_login import UserMixin

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    tup_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    section = db.Column(db.String(50), nullable=True)  # New field
    picture_path = db.Column(db.String(200), nullable=True)
    motorcycles = db.relationship('Motorcycle', backref='owner', lazy=True)

    def __repr__(self):
        return f'<Person {self.name}>'

class Motorcycle(db.Model):
    __tablename__ = 'motorcycles'
    
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(10), unique=True, nullable=False)
    model = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    vehicle_trackings = db.relationship('VehicleTracking', backref='motorcycle', lazy=True)

    def __repr__(self):
        return f'<Motorcycle {self.plate_number}>'

class VehicleTracking(db.Model):
    __tablename__ = 'vehicle_tracking'
    
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(10), db.ForeignKey('motorcycles.plate_number'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    mode = db.Column(db.String(10), nullable=False)  # 'in' or 'out'

    def __repr__(self):
        return f'<VehicleTracking {self.plate_number} {self.timestamp} {self.mode}>'

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Add additional fields as needed (e.g., email, etc.)

    def __repr__(self):
        return f'<User {self.username}>'
