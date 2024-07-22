from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motorcycles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Motorcycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), unique=True, nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    or_cr_number = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Motorcycle {self.plate_number}>'

class VehicleTracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), db.ForeignKey('motorcycle.plate_number'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<VehicleTracking {self.plate_number} at {self.timestamp}>'

with app.app_context():
    db.create_all()

@app.route('/motorcycles', methods=['POST'])
def add_motorcycle():
    data = request.get_json()
    new_motorcycle = Motorcycle(
        plate_number=data['plate_number'],
        owner=data['owner'],
        model=data['model'],
        or_cr_number=data['or_cr_number']
    )
    db.session.add(new_motorcycle)
    db.session.commit()
    return jsonify({'message': 'New motorcycle added'}), 201

@app.route('/vehicle_tracking', methods=['POST'])
def track_vehicle():
    data = request.get_json()
    plate_number = data.get('plate_number')
    
    # Check if the motorcycle is enrolled
    motorcycle = Motorcycle.query.filter_by(plate_number=plate_number).first()
    if not motorcycle:
        return jsonify({'message': 'Plate number not enrolled'}), 404
    
    new_tracking = VehicleTracking(
        plate_number=plate_number,
        timestamp=datetime.now()
    )
    print(f"Adding vehicle record : {new_tracking}")
    db.session.add(new_tracking)
    db.session.commit()
    return jsonify({'message': 'Vehicle tracking entry added'}), 201

@app.route('/motorcycles', methods=['GET'])
def get_motorcycles():
    motorcycles = Motorcycle.query.all()
    return jsonify([{
        'plate_number': motorcycle.plate_number,
        'owner': motorcycle.owner,
        'model': motorcycle.model,
        'or_cr_number': motorcycle.or_cr_number
    } for motorcycle in motorcycles])

@app.route('/vehicle_tracking', methods=['GET'])
def get_vehicle_tracking():
    tracking = VehicleTracking.query.all()
    return jsonify([{
        'plate_number': entry.plate_number,
        'timestamp': entry.timestamp
    } for entry in tracking])

if __name__ == '__main__':
    app.run(debug=True)
