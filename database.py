import sqlite3
from datetime import datetime

DB_NAME = "attendance.db"


# ==========================
# Create Database
# ==========================
def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Student Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        image_path TEXT
    )
    """)

    # Attendance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()


# ==========================
# Register Student
# ==========================
def register_student(name, image_path):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO students(name,image_path)
    VALUES(?,?)
    """, (name, image_path))

    conn.commit()
    conn.close()


# ==========================
# Mark Attendance
# ==========================
def mark_attendance(name):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    today = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%I:%M %p")

    cursor.execute("""
    SELECT * FROM attendance
    WHERE name=? AND date=?
    """, (name, today))

    data = cursor.fetchone()

    if data:
        conn.close()
        return False

    cursor.execute("""
    INSERT INTO attendance(name,date,time)
    VALUES(?,?,?)
    """, (name, today, current_time))

    conn.commit()
    conn.close()

    return True


# ==========================
# Get Students
# ==========================
def get_students():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================
# Get Attendance
# ==========================
def get_attendance():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM attendance
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================
# Total Students
# ==========================
def total_students():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")

    count = cursor.fetchone()[0]

    conn.close()

    return count


# ==========================
# Today's Attendance
# ==========================
def today_attendance():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    today = datetime.now().strftime("%d-%m-%Y")

    cursor.execute("""
    SELECT COUNT(*) FROM attendance
    WHERE date=?
    """, (today,))

    count = cursor.fetchone()[0]

    conn.close()

    return count


# ==========================
# Check Attendance
# ==========================
def check_attendance(name):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    today = datetime.now().strftime("%d-%m-%Y")

    cursor.execute("""
    SELECT * FROM attendance
    WHERE name=? AND date=?
    """, (name, today))

    data = cursor.fetchone()

    conn.close()

    return data is not None