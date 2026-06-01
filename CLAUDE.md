# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Run the application**: `python app.py` (runs on http://localhost:5001)
- **Run tests**: `pytest` (if tests are written) or `python -m pytest`
- **Install dependencies**: `pip install -r requirements.txt`

## Project Structure

- `app.py`: Main Flask application file containing route definitions and database initialization.
- `database/db.py`: Database layer with SQLite implementation, including connection handling, table initialization, and data seeding.
- `templates/`: HTML templates for the web pages (landing, login, register, terms, base).
- `static/`: Static assets (CSS, JavaScript).
- `expense_tracker.db`: SQLite database file (generated on first run).
- `requirements.txt`: Python dependencies.

## Architecture Overview

The application follows a simple Flask web application structure:

1. **Presentation Layer**: Flask routes in `app.py` render HTML templates.
2. **Data Layer**: SQLite database accessed via `database/db.py` using parameterized queries for security.
3. **Database Schema**: Two tables - `users` and `expenses` with a foreign key relationship.
4. **Initialization**: On app startup, the database is initialized and seeded with demo data if not already present.

## Key Functions in `database/db.py`

- `get_db()`: Returns a configured SQLite connection with row factory and foreign keys enabled.
- `init_db()`: Creates the `users` and `expenses` tables if they don't exist.
- `seed_db()`: Adds a demo user and sample expenses only if the database is empty.

## Common Development Tasks

- **Adding a new route**: Edit `app.py` and create a corresponding template in `templates/`.
- **Modifying database schema**: Edit the `init_db()` function in `database/db.py` and adjust `seed_db()` if needed.
- **Running the application**: Execute `python app.py` and visit `http://localhost:5001`.
- **Running tests**: Once tests are written, run `pytest` in the project root.

## Notes

- The application uses Flask and Werkzeug for password hashing.
- All SQL queries use parameterized statements to prevent SQL injection.
- The database file is stored in the project root as `expense_tracker.db`.