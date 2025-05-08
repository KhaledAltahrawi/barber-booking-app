import sqlite3
from flask import Flask, g

DATABASE = 'barber_appointments.db'
app = Flask(__name__)

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
            db.executescript(f.read())
        insert_initial_data(db)

def insert_initial_data(db):
    cursor = db.cursor()
    services = [
        ('Beard Trim', 30),
        ('Haircut', 30),
        ('Haircut & Beard Trim', 60)
    ]
    cursor.executemany("INSERT OR IGNORE INTO services (name, duration_minutes) VALUES (?, ?)", services)
    cursor.execute("INSERT OR IGNORE INTO barbers (username, password) VALUES (?, ?)", ('test_barber', 'password123'))
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.config['DATABASE'] = DATABASE
    with app.app_context():
        init_db()
    print("Database initialized successfully with initial data!")
