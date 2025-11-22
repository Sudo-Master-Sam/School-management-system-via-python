import sqlite3

DB_NAME = "school.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Students table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        student_class TEXT,
        phone TEXT,
        parent_name TEXT
    )
    """)

    # Teachers table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        subject TEXT,
        phone TEXT
    )
    """)

    # Uniforms table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS uniforms (
        uniform_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        size TEXT,
        quantity INTEGER,
        price REAL
    )
    """)

    # Stationery table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stationery (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        quantity INTEGER,
        price REAL
    )
    """)

    # Fees table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fees (
        fee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        month TEXT,
        date_issued TEXT,
        FOREIGN KEY(student_id) REFERENCES students(student_id)
    )
    """)

    # Receipts table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS receipts (
        receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        item_details TEXT,
        total_amount REAL,
        date_issued TEXT,
        FOREIGN KEY(student_id) REFERENCES students(student_id)
    )
    """)

    # Teacher Attendance table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS teacher_attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('Present','Absent')),
        FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id)
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized!")

if __name__ == "__main__":
    init_db()
