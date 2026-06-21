import sqlite3
from datetime import datetime

DB_NAME = "business.db"


def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        status TEXT NOT NULL,
        contact TEXT NOT NULL,
        created_date TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def insert_record(full_name, gender, status, contact):
    conn = connect_db()
    cursor = conn.cursor()

    created_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    INSERT INTO records
    (full_name, gender, status, contact, created_date)
    VALUES (?, ?, ?, ?, ?)
    """, (full_name, gender, status, contact, created_date))

    conn.commit()
    conn.close()


def get_all_records():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM records")

    data = cursor.fetchall()

    conn.close()

    return data


def search_records(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM records
    WHERE full_name LIKE ?
    OR status LIKE ?
    OR contact LIKE ?
    OR id LIKE ?
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    data = cursor.fetchall()

    conn.close()

    return data


def filter_records(gender, status):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM records
    WHERE gender = ?
    AND status = ?
    """, (gender, status))

    data = cursor.fetchall()

    conn.close()

    return data


def preload_records():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM records")

    count = cursor.fetchone()[0]

    if count == 0:

        sample_data = [

            ("John Kamara", "Male", "Active", "076111111"),
            ("Mariama Bangura", "Female", "Pending", "076111112"),
            ("Ibrahim Sesay", "Male", "Active", "076111113"),
            ("Fatmata Koroma", "Female", "Inactive", "076111114"),
            ("Mohamed Turay", "Male", "Active", "076111115"),
            ("Hawa Kanu", "Female", "Active", "076111116"),
            ("Abu Conteh", "Male", "Pending", "076111117"),
            ("Aminata Jalloh", "Female", "Active", "076111118"),
            ("Alhaji Kamara", "Male", "Inactive", "076111119"),
            ("Kadiatu Sesay", "Female", "Active", "076111120"),
            ("Musa Bangura", "Male", "Active", "076111121"),
            ("Isatu Koroma", "Female", "Pending", "076111122"),
            ("Sorie Conteh", "Male", "Active", "076111123"),
            ("Adama Turay", "Female", "Active", "076111124"),
            ("Abdul Kanu", "Male", "Inactive", "076111125"),
            ("Rugiatu Kamara", "Female", "Active", "076111126"),
            ("Ishmael Sesay", "Male", "Pending", "076111127"),
            ("Bintu Bangura", "Female", "Active", "076111128"),
            ("Alpha Koroma", "Male", "Active", "076111129"),
            ("Haja Conteh", "Female", "Active", "076111130")

        ]

        for row in sample_data:
            insert_record(*row)

    conn.close()


create_table()
preload_records()
