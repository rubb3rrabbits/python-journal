import sqlite3
from auth import hash_password, verify_password

DB_NAME = "journal.db"


def get_connection():
    """Returns a connection object to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Creates the necessary database tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Enable foreign keys in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Create the users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    """)

    # 2. Create the entries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()


def register_user(username, password):
    """Registers a new user with a hashed password."""
    hashed = hash_password(password)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # This triggers if the username already exists due to the UNIQUE constraint
        print("Error: Username already exists.")
        return False
    finally:
        conn.close()


def get_user(username):
    """Retrieves a user record by username."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,),
    )
    user = cursor.fetchone()
    conn.close()
    return user  # Returns a tuple (id, username, password_hash) or None

def create_entry(user_id, title, content):
    """Creates a new journal entry for a specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO entries (user_id, title, content) VALUES (?, ?, ?)",
        (user_id, title, content),
    )
    conn.commit()
    conn.close()


def get_entries(user_id):
    """Retrieves all journal entries for a given user, newest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, content, created_at 
        FROM entries 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    """,
        (user_id,),
    )
    entries = cursor.fetchall()
    conn.close()
    return entries  # Returns a list of tuples

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")

    # Test user registration (will print error if user already exists from last run, which is fine!)
    success = register_user("testuser", "securepassword123")
    if success:
        print("User registered successfully!")

    # Test fetching user
    user = get_user("testuser")
    print(f"Retrieved user from DB: {user}")

    if user:
        user_id = user[0]  # Grab the ID from the tuple (id, username, password_hash)

        # Test creating an entry
        create_entry(user_id, "My First Entry", "SQLite and Python are working smoothly!")
        print("Journal entry created!")

        # Test fetching entries
        entries = get_entries(user_id)
        print(f"Retrieved entries: {entries}")