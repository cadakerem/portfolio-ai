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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            morning_time TEXT,
            evening_time TEXT
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

def set_user_schedule(user_id, morning_time, evening_time):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_settings (user_id, morning_time, evening_time)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
        morning_time=excluded.morning_time,
        evening_time=excluded.evening_time
    ''', (user_id, morning_time, evening_time))
    conn.commit()
    conn.close()

def get_users_by_time(current_time):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # If a user has no settings, default to 10:15 and 17:45
    cursor.execute('''
        SELECT DISTINCT p.user_id 
        FROM portfolio p
        LEFT JOIN user_settings s ON p.user_id = s.user_id
        WHERE 
            (s.morning_time = ? OR s.evening_time = ?)
            OR 
            (s.user_id IS NULL AND (? = '10:15' OR ? = '17:45'))
    ''', (current_time, current_time, current_time, current_time))
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users
