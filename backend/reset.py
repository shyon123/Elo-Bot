from my_database import get_connection

def reset_db(db_file="elo2.db"):
    with get_connection(db_file) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Matches")
        c.execute("DELETE FROM Players")
        conn.commit()
    print(f"{db_file} has been reset.")

if __name__ == "__main__":
    reset_db()
