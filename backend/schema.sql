-- Drop existing tables (if any)
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS barbers;
DROP TABLE IF EXISTS available_slots;
DROP TABLE IF EXISTS appointments;

-- Customers
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone_number TEXT NOT NULL UNIQUE
);

-- Services
CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL
);

-- Barbers (Single barber for now)
CREATE TABLE barbers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- Availability Slots (TODO: Implement merging logic)
CREATE TABLE available_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barber_id INTEGER NOT NULL DEFAULT 1,
    day TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    FOREIGN KEY (barber_id) REFERENCES barbers(id)
);

-- Appointments
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    appointment_datetime TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    cancellation_reason TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (service_id) REFERENCES services(id)
);

-- Initial Data
INSERT INTO barbers (username, password) VALUES 
    ('admin', 'temp_password'); -- TODO: Add hashing

INSERT INTO services (name, duration_minutes) VALUES 
    ('Haircut', 30),
    ('Beard Trim', 30),
    ('Haircut & Beard Combo', 60);