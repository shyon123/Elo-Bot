import file_processor
import search
import my_database
def main():
    db_file = "elo2.db"
    my_database.init_db()
    file_processor.ingest_file("input_file.txt", db_file=db_file)
    search.show_top_players(db_file=db_file)

if __name__ == "__main__":
    main()