import sqlite3
import pandas as pd

def add_transaction(user_id, type_, category, amount, date):
    conn = sqlite3.connect("sample_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, ?, ?, ?, ?)",
              (user_id, type_, category, amount, date))
    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = sqlite3.connect("sample_data.db")
    df = pd.read_sql_query("SELECT * FROM transactions WHERE user_id=?", conn, params=(user_id,))
    conn.close()
    return df
