# app/vehicle_tracking/views.py
from . import vehicle_tracking_blueprint
from flask import render_template, request, flash, redirect, url_for
from app.models import VehicleTracking
from app.extensions import db
from sqlalchemy import and_
from datetime import datetime
from flask_login import login_required

@vehicle_tracking_blueprint.route("/")
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    plate_number = request.args.get('plate_number', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query = VehicleTracking.query

    if plate_number:
        query = query.filter(VehicleTracking.plate_number.like(f'%{plate_number}%'))
    if start_date:
        query = query.filter(VehicleTracking.timestamp >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(VehicleTracking.timestamp <= datetime.strptime(end_date, '%Y-%m-%d'))

    vehicle_trackings = query.order_by(VehicleTracking.timestamp.desc()).paginate(page=page, per_page=10)
    return render_template('list_tracking.html', trackings=vehicle_trackings)

@vehicle_tracking_blueprint.route("/search", methods=["GET"])
@login_required
def search():
    plate_number = request.args.get('plate_number', '', type=str)
    start_date = request.args.get('start_date', '', type=str)
    end_date = request.args.get('end_date', '', type=str)
    page = request.args.get('page', 1, type=int)

    query = VehicleTracking.query

    if plate_number:
        query = query.filter(VehicleTracking.plate_number.ilike(f'%{plate_number}%'))

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(and_(VehicleTracking.timestamp >= start_date, VehicleTracking.timestamp <= end_date))
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.")

    vehicle_trackings = query.paginate(page=page, per_page=10)
    return render_template('list_tracking.html', trackings=vehicle_trackings)

@vehicle_tracking_blueprint.route("/view/<int:tracking_id>")
@login_required
def view_tracking(tracking_id):
    tracking = VehicleTracking.query.get_or_404(tracking_id)
    return render_template("view_vehicle_tracking.html", tracking=tracking)
