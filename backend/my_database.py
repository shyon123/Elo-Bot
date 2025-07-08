import sqlite3

def get_connection(db_file="elo.db"):
    return sqlite3.connect(db_file)

def init_db(db_file="elo.db"):
    with get_connection(db_file) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Players (
                        name TEXT PRIMARY KEY,
                        rating REAL DEFAULT 1000)''')
        c.execute('''CREATE TABLE IF NOT EXISTS Matches (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player1 TEXT,
                        player2 TEXT,
                        result INTEGER,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()