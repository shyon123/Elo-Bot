import my_database as db 
import elo_calc

def process_match(p1, p2, result, db_file="elo.db"):
    with db.get_connection(db_file) as conn:
        c = conn.cursor()

        # Ensure both players exist
        for player in [p1, p2]:
            c.execute("INSERT OR IGNORE INTO Players (name) VALUES (?)", (player,))

        # Get current ratings
        c.execute("SELECT rating FROM Players WHERE name=?", (p1,))
        r1 = c.fetchone()[0]
        c.execute("SELECT rating FROM Players WHERE name=?", (p2,))
        r2 = c.fetchone()[0]

        # Update Elo
        r1_new, r2_new = elo_calc.update_elo(r1, r2, result)

        # Save new ratings and match
        c.execute("UPDATE Players SET rating=? WHERE name=?", (r1_new, p1))
        c.execute("UPDATE Players SET rating=? WHERE name=?", (r2_new, p2))
        c.execute("INSERT INTO Matches (player1, player2, result) VALUES (?, ?, ?)", (p1, p2, result))
        conn.commit()

def ingest_file(file_path, db_file="elo.db"):
    db.init_db(db_file)
    with open(file_path) as f:
        for line in f:
            p1, p2, res = line.strip().split(",")
            process_match(p1.strip(), p2.strip(), int(res.strip()), db_file=db_file)


