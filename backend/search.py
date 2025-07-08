import my_database as db 

import sqlite3

def show_top_players(db_file, n=100):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    n = int(n)  # Ensures LIMIT gets an integer
    c.execute("SELECT name, rating FROM Players ORDER BY rating DESC LIMIT ?", (n,))
    rows = c.fetchall()
    conn.close()
    return [{"name": row[0], "rating": row[1]} for row in rows]


def search_player(name, db_file="elo.db"):
    with db.get_connection(db_file) as conn:
        c = conn.cursor()
        c.execute("SELECT rating FROM Players WHERE name=?", (name,))
        result = c.fetchone()
        if not result:
            print("Player not found.")
            return
        print(f"{name}: Elo {round(result[0])}")

        c.execute("SELECT * FROM Matches WHERE player1=? OR player2=? ORDER BY timestamp DESC", (name, name))
        matches = c.fetchall()
        for m in matches:
            print(f"vs {m[2] if m[1] == name else m[1]} | Result: {m[3]} | Time: {m[4]}")