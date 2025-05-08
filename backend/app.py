from flask import Flask, jsonify, request
from database import get_db
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Welcome to the Barber Appointment Booking API!'

@app.route('/services')
def get_services():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name, duration_minutes FROM services")
    services = cursor.fetchall()
    db.close()
    return jsonify([dict(row) for row in services])

@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    customer_name = data.get('customer_name')
    phone_number = data.get('phone_number')
    service_id = data.get('service_id')
    appointment_datetime = data.get('appointment_datetime')

    if not all([customer_name, phone_number, service_id, appointment_datetime]):
        return jsonify({'error': 'Missing required fields'}), 400

    db = get_db()
    cursor = db.cursor()

    # Check if customer exists
    cursor.execute("SELECT id FROM customers WHERE phone_number = ?", (phone_number,))
    customer = cursor.fetchone()
    if not customer:
        cursor.execute("INSERT INTO customers (name, phone_number) VALUES (?, ?)", (customer_name, phone_number))
        customer_id = cursor.lastrowid
    else:
        customer_id = customer['id']

    # Insert the appointment
    cursor.execute("INSERT INTO appointments (customer_id, service_id, appointment_datetime, status) VALUES (?, ?, ?, ?)",
                    (customer_id, service_id, appointment_datetime, 'pending'))
    db.commit()

    # Retrieve the newly created appointment
    appointment_id = cursor.lastrowid
    cursor.execute("SELECT a.id, c.name AS customer_name, c.phone_number, s.name AS service_name, a.appointment_datetime, a.status "
                    "FROM appointments a JOIN customers c ON a.customer_id = c.id "
                    "JOIN services s ON a.service_id = s.id WHERE a.id = ?", (appointment_id,))
    new_appointment = cursor.fetchone()
    db.close()

    return jsonify({
        'message': 'Appointment created successfully!',
        'appointment': dict(new_appointment)
    }), 201

@app.route('/available_slots', methods=['POST'])
def add_available_slot():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    barber_id = 1  # Assuming a single barber for now
    day = data.get('day')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not all([day, start_time, end_time]):
        return jsonify({'error': 'Missing required fields'}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO available_slots (barber_id, day, start_time, end_time) VALUES (?, ?, ?, ?)",
                       (barber_id, day, start_time, end_time))
        db.commit()
        return jsonify({'message': 'Available slot added successfully!'}), 201
    except sqlite3.Error as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/appointments', methods=['GET'])
def get_appointments():
    status = request.args.get('status')
    db = get_db()
    cursor = db.cursor()
    query = """
        SELECT a.id, c.name AS customer_name, c.phone_number, s.name AS service_name,
               a.appointment_datetime, a.status, a.cancellation_reason
        FROM appointments a
        JOIN customers c ON a.customer_id = c.id
        JOIN services s ON a.service_id = s.id
    """
    params = ()
    if status:
        query += " WHERE a.status = ?"
        params = (status,)

    cursor.execute(query, params)
    appointments = cursor.fetchall()
    db.close()
    return jsonify([dict(row) for row in appointments])

@app.route('/appointments/<int:appointment_id>', methods=['PUT'])
@app.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment_status(appointment_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    status = data.get('status')
    cancellation_reason = data.get('cancellation_reason') # Get cancellation reason

    if not status:
        return jsonify({'error': 'Missing status'}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        if status == 'cancelled':
            cursor.execute("UPDATE appointments SET status = ?, cancellation_reason = ? WHERE id = ?", (status, cancellation_reason, appointment_id)) #update with reason
        else:
            cursor.execute("UPDATE appointments SET status = ? WHERE id = ?", (status, appointment_id))
        db.commit()
        if cursor.rowcount > 0:
            # In a real application, you might want to send an SMS notification to the customer here
            return jsonify({'message': f'Appointment status updated to {status}'}), 200
        else:
            return jsonify({'error': 'Appointment not found'}), 404
    except sqlite3.Error as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/login', methods=['POST'])
def login_barber():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM barbers WHERE username = ? AND password = ?", (username, password))
    barber = cursor.fetchone()
    db.close()

    if barber:
        return jsonify({'message': 'Login successful!', 'barber_id': barber['id']}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)
