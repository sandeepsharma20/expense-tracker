---
# Spec: Registration

## Overview
This feature implements user registration functionality for the Spendly expense tracker. Users can create new accounts by providing their name, email, and password. The system validates the input, checks for existing emails, securely hashes passwords using Werkzeug, and stores new user records in the SQLite database. This enables users to access personalized features like expense tracking after registration.

## Depends on
This feature depends on the database setup (step -1) which created the users table with appropriate schema including email uniqueness constraint and password hash storage.

## Routes
- `POST /register` — Process registration form submission, validate input, create new user — public
- `GET /register` — Display registration form — public (already exists but will be modified to handle both GET and POST)

## Database changes
No database changes. The users table already exists with the required schema (id, name, email, password_hash, created_at) including UNIQUE constraint on email.

## Templates
- **Create:** None (register.html already exists)
- **Modify:** 
  - `templates/register.html` — Add CSS classes for error/success flash messages display

## Files to change
- `app.py` — Add POST handling to /register route, implement validation, database insertion, flash messages, and redirects
- `templates/register.html` — Add placeholders for displaying flash messages (error and success)

## Files to create
- None

## New dependencies
No new dependencies. Uses existing Flask, Werkzeug (for password hashing), and SQLite3 libraries.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw SQL with parameterized queries only
- Passwords hashed with werkzeug.security.generate_password_hash
- All SQL queries must use parameterized statements to prevent SQL injection
- Use CSS variables from existing stylesheet — never hardcode hex values
- All templates extend base.html (register.html already does)
- Implement proper input validation (required fields, email format)
- Check for existing email before creating new user
- Provide user feedback via flash messages for both success and error cases
- Redirect to login page after successful registration
- Use Flask session only after login (not for registration itself)

## Definition of done
- User can access registration form at /register via GET request
- Registration form validates that name, email, and password are required
- Registration form rejects submission if email already exists in database
- New user is created in database with properly hashed password when validation passes
- User sees appropriate success message after successful registration
- User sees appropriate error messages for validation failures
- After successful registration, user is redirected to login page
- Password is never stored in plain text in database
- All database queries use parameterized statements
- Existing login and landing pages continue to work unchanged