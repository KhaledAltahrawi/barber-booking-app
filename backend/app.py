from flask import Flask, jsonify, request
from database import get_db
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
CORS(app)

# ----- Core Routes -----
@app.route('/services', methods=['GET'])
def get_services():
    """Get all services"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name, duration_minutes FROM services")
    services = cursor.fetchall()
    db.close()
    return jsonify([dict(row) for row in services])

@app.route('/barber/login', methods=['POST'])
def barber_login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing credentials'}), 400

    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT id, password FROM barbers WHERE username = ?", (username,))
        barber = cursor.fetchone()
        
        if barber and check_password_hash(barber['password'], password):
            return jsonify({
                'message': 'Login successful',
                'barber_id': barber['id'],
                'token': 'sample_jwt_token'  # In production, use proper JWT
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
        
@app.route('/appointments', methods=['POST'])
def create_appointment():
    """Create new appointment with conflict check"""
    data = request.get_json()
    
    # Validation
    required = ['customer_name', 'phone_number', 'service_id', 'appointment_datetime']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400

    db = get_db()
    cursor = db.cursor()

    try:
        # 1. Get service duration
        cursor.execute("SELECT duration_minutes FROM services WHERE id=?", (data['service_id'],))
        service = cursor.fetchone()
        if not service:
            return jsonify({'error': 'Invalid service ID'}), 400
        duration = service['duration_minutes']

        # 2. Check slot availability (TODO: Integrate with available_slots table)
        start_time = data['appointment_datetime']
        end_time = (datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + 
                   timedelta(minutes=duration)).strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            SELECT 1 FROM appointments 
            WHERE appointment_datetime BETWEEN ? AND ?
            AND status != 'cancelled'
        """, (start_time, end_time))
        if cursor.fetchone():
            return jsonify({'error': 'Time slot already booked'}), 400

        # 3. Create appointment
        cursor.execute("""
            INSERT INTO appointments 
            (customer_id, service_id, appointment_datetime, status)
            VALUES (?, ?, ?, 'pending')
        """, (1, data['service_id'], start_time))  # TODO: Dynamic customer_id
        db.commit()
        return jsonify({'message': 'Appointment booked!'}), 201

    except sqlite3.Error as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

        
        

# TODO: Add routes for:
# - Barber login
# - Availability management
# - Appointment status updates

if __name__ == '__main__':
    app.run(debug=True)