import logging
import sqlite3

con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                uid INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0
            )''')
con.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS Tasks (
                idofTask INTEGER PRIMARY KEY,
                description VARCHAR(50)
            )''')
con.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS UsersAndTasks (
                uid INTEGER,
                idofTask INTEGER,
                status TEXT DEFAULT 'none',
                PRIMARY KEY(uid, idofTask),
                FOREIGN KEY(uid) REFERENCES Users(uid) ON DELETE CASCADE,
                FOREIGN KEY(idofTask) REFERENCES Tasks(idofTask) ON DELETE CASCADE
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

tasks = [
    (1, 'Натиснути на кнопку додати 3 рази'),
    (2, 'Під\'єднати криптогаманець'),
    (3, 'Увійти до аккаунту')
]

cur.executemany('INSERT OR IGNORE INTO Tasks (idofTask, description) VALUES (?, ?)', tasks)
con.commit()

#cur.execute('SELECT * FROM Tasks')
#all_tasks = cur.fetchall()
#for task in all_tasks:
#    print(task)

#con.close()

def get_user_quest_status(uid):
    cur.execute('SELECT idofTask, status FROM UsersAndTasks WHERE uid = ?', (uid,))
    results = cur.fetchall()
    if not results:
        return []
    status_list = [{'idofTask': task_id, 'status': status} for task_id, status in results]
    return status_list

def update_user_quest_status(uid, idofTask, status):
    cur.execute('REPLACE INTO UsersAndTasks (uid, idofTask, status) VALUES (?, ?, ?)', (uid, idofTask, status))
    con.commit()


def add_new_user(uid):
    cur.execute('INSERT INTO Users (uid, balance) VALUES (?, ?)', (uid, 0))
    initial_status = False
    cur.execute('INSERT INTO UsersAndTasks (uid, idofTask, status) VALUES (?, ?, ?)', (uid, 1, initial_status))
    cur.execute('INSERT INTO UsersAndTasks (uid, idofTask, status) VALUES (?, ?, ?)', (uid, 2, initial_status))
    cur.execute('INSERT INTO UsersAndTasks (uid, idofTask, status) VALUES (?, ?, ?)', (uid, 3, initial_status))
    con.commit()
