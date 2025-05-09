import sqlite3
from werkzeug.security import generate_password_hash
from flask import g

DATABASE = 'barber_appointments.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        seed_initial_data(db)

def seed_initial_data(db):
    cursor = db.cursor()
    # Barber with hashed password
    cursor.execute(
        "INSERT INTO barbers (username, password) VALUES (?, ?)",
        ('admin', generate_password_hash('temp_password'))
    )
    # Services
    cursor.executemany(
        "INSERT INTO services (name, duration_minutes) VALUES (?, ?)",
        [
            ('Haircut', 30),
            ('Beard Trim', 30),
            ('Haircut & Beard Combo', 60)
        ]
    )
    db.commit()

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    init_db()
    print("Database initialized with:")
    print("- Admin user: admin/temp_password")
    print("- 3 services")