import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        conn = sqlite3.connect("sample_data.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("sample_data.db")
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
