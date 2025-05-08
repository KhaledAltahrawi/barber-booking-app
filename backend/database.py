import sqlite3

DATABASE = 'barber_appointments.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create barbers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS barbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL UNIQUE
        )
    ''')

    # Create services table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            duration_minutes INTEGER NOT NULL
        )
    ''')

    # Create available_slots table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS available_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barber_id INTEGER NOT NULL,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            FOREIGN KEY (barber_id) REFERENCES barbers(id)
        )
    ''')

    cursor.execute('''
         CREATE TABLE IF NOT EXISTS appointments (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         customer_id INTEGER NOT NULL,
         service_id INTEGER NOT NULL,
         appointment_datetime DATETIME NOT NULL,
         status TEXT NOT NULL DEFAULT 'pending', 
         FOREIGN KEY (customer_id) REFERENCES customers(id),
         FOREIGN KEY (service_id) REFERENCES services(id)
         )
         ''')

    # Insert initial services
    services = [
        ('Beard Trim', 30),
        ('Haircut', 30),
        ('Haircut & Beard Trim', 60)
    ]
    cursor.executemany("INSERT OR IGNORE INTO services (name, duration_minutes) VALUES (?, ?)", services)

    # Insert a default barber
    cursor.execute("INSERT OR IGNORE INTO barbers (username, password) VALUES (?, ?)", ('test_barber', 'password123'))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully with initial data!")