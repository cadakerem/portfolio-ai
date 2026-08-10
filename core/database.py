import sqlite3
from core.config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            user_id INTEGER,
            ticker TEXT,
            amount REAL,
            avg_price REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_or_update_asset(user_id, ticker, amount, avg_price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT amount, avg_price FROM portfolio WHERE user_id=? AND ticker=?", (user_id, ticker))
    row = cursor.fetchone()
    
    if row:
        old_amount, old_price = row
        new_amount = old_amount + amount
        new_avg = ((old_amount * old_price) + (amount * avg_price)) / new_amount
        cursor.execute("UPDATE portfolio SET amount=?, avg_price=? WHERE user_id=? AND ticker=?", 
                       (new_amount, new_avg, user_id, ticker))
    else:
        cursor.execute("INSERT INTO portfolio (user_id, ticker, amount, avg_price) VALUES (?, ?, ?, ?)", 
                       (user_id, ticker, amount, avg_price))
        
    conn.commit()
    conn.close()

def remove_asset(user_id, ticker):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM portfolio WHERE user_id=? AND ticker=?", (user_id, ticker))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted > 0

def get_portfolio(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ticker, amount, avg_price FROM portfolio WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT user_id FROM portfolio")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users
