     DROP TABLE IF EXISTS customers;
     DROP TABLE IF EXISTS services;
     DROP TABLE IF EXISTS barbers;
     DROP TABLE IF EXISTS available_slots;
     DROP TABLE IF EXISTS appointments;

     CREATE TABLE customers (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         phone_number TEXT NOT NULL UNIQUE
     );

     CREATE TABLE services (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         duration_minutes INTEGER NOT NULL
     );

     CREATE TABLE barbers (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         username TEXT NOT NULL UNIQUE,
         password TEXT NOT NULL
     );

     CREATE TABLE available_slots (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         barber_id INTEGER NOT NULL,
         day TEXT NOT NULL,
         start_time TEXT NOT NULL,
         end_time TEXT NOT NULL,
         FOREIGN KEY (barber_id) REFERENCES barbers(id)
     );

     CREATE TABLE appointments (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         customer_id INTEGER NOT NULL,
         service_id INTEGER NOT NULL,
         appointment_datetime DATETIME NOT NULL,
         status TEXT NOT NULL DEFAULT 'pending',
         cancellation_reason TEXT,
         FOREIGN KEY (customer_id) REFERENCES customers(id),
         FOREIGN KEY (service_id) REFERENCES services(id)
     );
     