import logging
import sqlite3

con = sqlite3.connect('db.sqlite', check_same_thread=False)
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                uid INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0
            )''')
con.commit()

def add_user(uid):
    # new user always has balance = 0
    cur.execute('INSERT INTO Users (uid) VALUES (?)', (uid,))
    con.commit()

def check_user(uid):
    cur.execute('SELECT * FROM Users WHERE uid = ?', (uid,))
    user = cur.fetchone()
    return bool(user)

def add_balance(uid, amount):
    cur.execute('UPDATE Users SET balance = balance + ? WHERE uid = ?', (amount, uid))
    con.commit()

def get_balance(uid):
    cur.execute('SELECT balance FROM Users WHERE uid = ?', (uid,))
    result = cur.fetchone()
    if result is None:
        logging.info(f'User {uid} not found in database. Returning balance: 0')
        return 0
    balance = result[0]
    logging.info(f'User {uid} balance: {balance}')
    return balance
