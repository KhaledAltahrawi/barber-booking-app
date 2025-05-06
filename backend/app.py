from flask import Flask, jsonify, request
from database import get_db
from flask_cors import CORS  # استيراد CORS

app = Flask(__name__)
CORS(app)  # تمكين CORS لجميع المسارات (للتطوير فقط)

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
    cursor.execute("INSERT INTO appointments (customer_id, service_id, appointment_datetime) VALUES (?, ?, ?)",
                   (customer_id, service_id, appointment_datetime))
    db.commit()

    # Retrieve the newly created appointment
    appointment_id = cursor.lastrowid
    cursor.execute("SELECT a.id, c.name AS customer_name, c.phone_number, s.name AS service_name, a.appointment_datetime "
                   "FROM appointments a JOIN customers c ON a.customer_id = c.id "
                   "JOIN services s ON a.service_id = s.id WHERE a.id = ?", (appointment_id,))
    new_appointment = cursor.fetchone()
    db.close()

    return jsonify({
        'message': 'Appointment created successfully!',
        'appointment': dict(new_appointment)
    }), 201

if __name__ == '__main__':
    app.run(debug=True)