import sqlite3


def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY, 
                       city TEXT)''')
    conn.commit()
    conn.close()


def add_user_city(user_id, city):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (id, city) VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET city=excluded.city',
                   (user_id, city))
    conn.commit()
    conn.close()


def get_city_by_user_id(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT city FROM users WHERE id = ?', (user_id,))
    city = cursor.fetchone()
    conn.close()
    return city[0] if city else None

