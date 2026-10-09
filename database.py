import sqlite3

DB_NAME = 'journal.db'

def get_connection():
    """Returns a connection object to the SQLite database."""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Creates the necessary database tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Enable foreign keys in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # TODO: Execute CREATE TABLE IF NOT EXISts queries for 'users' and entries'


    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initalized successfully!")

