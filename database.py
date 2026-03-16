import sqlite3
from datetime import datetime, timedelta

DB_PATH = "triplebot.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            registered_date TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            feedback_submitted INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_user(email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(email, password_hash):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now()
    expiry = now + timedelta(days=10)
    c.execute('''
        INSERT INTO users (email, password_hash, registered_date, expiry_date)
        VALUES (?, ?, ?, ?)
    ''', (email, password_hash, now.strftime("%Y-%m-%d"), expiry.strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def extend_expiry(email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    user = get_user(email)
    if user:
        current_expiry = datetime.strptime(user[4], "%Y-%m-%d")
        new_expiry = current_expiry + timedelta(days=15)
        c.execute('''
            UPDATE users SET expiry_date = ?, feedback_submitted = 1
            WHERE email = ?
        ''', (new_expiry.strftime("%Y-%m-%d"), email))
        conn.commit()
    conn.close()

def is_expired(email):
    user = get_user(email)
    if not user:
        return True
    expiry = datetime.strptime(user[4], "%Y-%m-%d")
    return datetime.now() > expiry