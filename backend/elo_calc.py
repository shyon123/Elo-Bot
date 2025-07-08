import my_database as db

def update_elo(r1, r2, result, k=32):
    expected1 = 1 / (1 + 10 ** ((r2 - r1) / 400))
    score1 = {0: 0.5, 1: 1.0, 2: 0.0}[result]
    score2 = 1.0 - score1
    r1_new = r1 + k * (score1 - expected1)
    r2_new = r2 + k * (score2 - (1 - expected1))
    return round(r1_new, 2), round(r2_new, 2)

def process_match(player1, player2, result, db_file="elo.db"):
    with db.get_connection(db_file) as conn:
        c = conn.cursor()

        # Get or create players
        for player in [player1, player2]:
            c.execute("INSERT OR IGNORE INTO Players (name, rating) VALUES (?, ?)", (player, 1000))

        # Get current ratings
        c.execute("SELECT rating FROM Players WHERE name=?", (player1,))
        r1 = c.fetchone()[0]
        c.execute("SELECT rating FROM Players WHERE name=?", (player2,))
        r2 = c.fetchone()[0]

        # Update ratings
        new_r1, new_r2 = update_elo(r1, r2, int(result))

        # Store updated ratings
        c.execute("UPDATE Players SET rating=? WHERE name=?", (new_r1, player1))
        c.execute("UPDATE Players SET rating=? WHERE name=?", (new_r2, player2))

        # Store match record
        c.execute("""
            INSERT INTO Matches (player1, player2, result, timestamp)
            VALUES (?, ?, ?, datetime('now'))
        """, (player1, player2, int(result)))

        conn.commit()