import sqlite3
from werkzeug.security import generate_password_hash
import os
import random
from datetime import datetime

# Import the get_db function from our database module
from database.db import get_db

def generate_indian_name():
    """Generate a random Indian first and last name."""
    first_names = [
        'Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Reyansh', 'Krishna',
        'Ishaan', 'Shaurya', 'Atharv', 'Naisha', 'Aanya', 'Ananya', 'Diya', 'Pihu',
        'Prisha', 'Kiara', 'Navya', 'Anika', 'Rohit', 'Mohit', 'Rahul', 'Priya',
        'Neha', 'Pooja', 'Anjali', 'Sneha', 'Kavya', 'Deepika', 'Sonam', 'Aishwarya'
    ]
    last_names = [
        'Sharma', 'Verma', 'Gupta', 'Agarwal', 'Reddy', 'Iyengar', 'Naidu', 'Pillai',
        'Kumar', 'Singh', 'Kaur', 'Patil', 'Deshmukh', 'Joshi', 'Kulkarni', 'Varma',
        'Mehta', 'Kapoor', 'Khanna', 'Malhotra', 'Chopra', 'Bansal', 'Jain', 'Mirza',
        'Khan', 'Shaikh', 'Ansari', 'Siddiqui', 'Farooqui'
    ]
    first = random.choice(first_names)
    last = random.choice(last_names)
    return first, last

def generate_email(first, last):
    """Generate email from first and last name with random 2-3 digit number."""
    # Convert to lowercase and remove spaces
    first_lower = first.lower()
    last_lower = last.lower()
    # Generate random 2 or 3 digit number
    rand_num = random.randint(10, 999)
    # Use gmail.com as per example
    email = f"{first_lower}.{last_lower}{rand_num}@gmail.com"
    return email

def email_exists(conn, email):
    """Check if email already exists in users table."""
    cursor = conn.execute('SELECT 1 FROM users WHERE email = ?', (email,))
    return cursor.fetchone() is not None

def main():
    conn = get_db()
    try:
        # Generate unique email
        while True:
            first, last = generate_indian_name()
            email = generate_email(first, last)
            if not email_exists(conn, email):
                break

        # Hash password
        password_hash = generate_password_hash('password123')
        current_time = datetime.now().isoformat()

        # Insert user
        cursor = conn.execute('''
            INSERT INTO users (name, email, password_hash, created_at)
            VALUES (?, ?, ?, ?)
        ''', (f"{first} {last}", email, password_hash, current_time))

        user_id = cursor.lastrowid
        conn.commit()

        # Print confirmation
        print(f"User created successfully:")
        print(f"ID: {user_id}")
        print(f"Name: {first} {last}")
        print(f"Email: {email}")

    finally:
        conn.close()

if __name__ == '__main__':
    main()