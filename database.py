"""
Smart Library Assistant - Database Module
SQLite Database connection, schema setup, and query helpers.
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "library.db")

def get_connection():
    """Returns a connection to the SQLite database with row factory enabled."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes tables if they do not exist."""
    conn = get_connection()
    cur = conn.cursor()

    # 1. Books Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            year INTEGER,
            description TEXT
        )
    """)

    # 2. Users Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    # 3. Borrow History Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS borrow_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            borrowed_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    # 4. Book Relationships Table (Graph Edges)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS book_relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id_1 INTEGER NOT NULL,
            book_id_2 INTEGER NOT NULL,
            relationship_type TEXT NOT NULL,
            strength REAL NOT NULL,
            FOREIGN KEY (book_id_1) REFERENCES books(id),
            FOREIGN KEY (book_id_2) REFERENCES books(id),
            UNIQUE(book_id_1, book_id_2, relationship_type)
        )
    """)

    conn.commit()
    conn.close()

def is_database_seeded():
    """Checks if the database has already been seeded with sample books."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM books")
        count = cur.fetchone()[0]
        return count >= 100
    except sqlite3.OperationalError:
        return False
    finally:
        conn.close()
