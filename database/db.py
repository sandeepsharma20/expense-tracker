import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

def get_db():
    """Create and return a database connection with proper configuration."""
    # Database file in project root
    db_path = os.path.join(os.path.dirname(__file__), '..', 'expense_tracker.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like access
    conn.execute('PRAGMA foreign_keys = ON')  # Enable foreign key constraints
    return conn

def init_db():
    """Initialize the database by creating tables if they don't exist."""
    conn = get_db()
    try:
        # Create users table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        ''')

        # Create expenses table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()
    finally:
        conn.close()

def seed_db():
    """Seed the database with initial demo data if it doesn't already exist."""
    conn = get_db()
    try:
        # Check if we already have users
        cursor = conn.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]

        if count > 0:
            # Database already seeded, return early
            return

        # Hash the password for demo user
        password_hash = generate_password_hash('demo123')

        # Insert demo user
        cursor = conn.execute('''
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
        ''', ('Demo User', 'demo@spendly.com', password_hash))

        user_id = cursor.lastrowid

        # Define expense data - 8 expenses covering all categories
        expenses_data = [
            # Food (2 expenses)
            (user_id, 12.50, 'Food', '2024-01-15', 'Lunch at cafe'),
            (user_id, 25.00, 'Food', '2024-01-10', 'Groceries for week'),
            # Transport (2 expenses)
            (user_id, 15.00, 'Transport', '2024-01-12', 'Bus ticket'),
            (user_id, 40.00, 'Transport', '2024-01-05', 'Gas fill up'),
            # Bills (1 expense)
            (user_id, 85.00, 'Bills', '2024-01-01', 'Electricity bill'),
            # Health (1 expense)
            (user_id, 30.00, 'Health', '2024-01-18', 'Pharmacy purchase'),
            # Entertainment (1 expense)
            (user_id, 20.00, 'Entertainment', '2024-01-14', 'Movie tickets'),
            # Shopping (1 expense)
            (user_id, 60.00, 'Shopping', '2024-01-08', 'New clothes')
        ]

        # Insert expenses using parameterized queries
        conn.executemany('''
            INSERT INTO expenses (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', expenses_data)

        conn.commit()
    finally:
        conn.close()