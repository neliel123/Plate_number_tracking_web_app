from . import api_blueprint
from flask import request, jsonify
from app.models import Motorcycle, VehicleTracking
from datetime import datetime, date
from app.extensions import db, socketio
from sqlalchemy import func

def count_today_vehicle_tracking():
    today = date.today()
    return db.session.query(func.count(VehicleTracking.id)).filter(
        func.date(VehicleTracking.timestamp) == today
    ).scalar()

@api_blueprint.route('/vehicle_tracking', methods=['POST'])
def track_vehicle():
    data = request.get_json()
    plate_number = data.get('plate_number')
    mode = data.get('mode')
    
    # Check if the motorcycle is enrolled
    motorcycle = Motorcycle.query.filter_by(plate_number=plate_number).first()
    if not motorcycle:
        return jsonify({'message': 'Plate number not enrolled'}), 404
    
    # Get the owner's picture path from the associated Student object
    owner = motorcycle.owner
    owner_info = {
        "tup_id": owner.tup_id,
        "last_name": owner.last_name,
        "first_name": owner.first_name,
        "picture_url": owner.picture_path,
        "section": owner.section
    } if owner else None
    
    new_tracking = VehicleTracking(
        plate_number=plate_number,
        timestamp=datetime.now(),
        mode=mode
    )
    db.session.add(new_tracking)
    db.session.commit()

    # Get the count of today's tracked vehicles
    count = count_today_vehicle_tracking()

    socketio.emit("updateMotorcycleTracking", {
        "isError": "false",
        "plate_number": motorcycle.plate_number,
        "owner": owner_info,
        "model": motorcycle.model,
        "count": count
    })
    return jsonify({'message': 'Vehicle tracking entry added'}), 201
