import sqlite3

conn = sqlite3.connect("immunization_emr.db")
cursor = conn.cursor()

# Patients table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT UNIQUE,
    child_name TEXT,
    dob TEXT,
    sex TEXT,
    mother_name TEXT,
    address TEXT,
    barangay TEXT,
    contact TEXT
)
""")

# Immunization table
cursor.execute("""
CREATE TABLE IF NOT EXISTS immunizations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT,
    vaccine TEXT,
    dose TEXT,
    date_given TEXT,
    given_by TEXT,
    remarks TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database created successfully")
