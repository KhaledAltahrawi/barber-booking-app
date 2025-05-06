from flask import Flask, jsonify
from database import get_db

app = Flask(__name__) 

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

if __name__ == '__main__':
    app.run(debug=True)