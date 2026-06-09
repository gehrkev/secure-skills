from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

def init_db():
    """Initialize the database with users table."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            token_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_token(token):
    """Hash a token using SHA256."""
    return hashlib.sha256(token.encode()).hexdigest()

def add_test_user(username, token):
    """Add a test user to the database."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    token_hash = hash_token(token)
    try:
        cursor.execute(
            'INSERT INTO users (username, token_hash) VALUES (?, ?)',
            (username, token_hash)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    """
    Login endpoint that accepts username and token in JSON request body.
    Verifies credentials against the database and returns appropriate JSON response.
    """
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"message": "Authentication failed"}), 401

        username = data.get('username', '')
        token = data.get('token', '')

        if not username or not token:
            return jsonify({"message": "Authentication failed"}), 401

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        token_hash = hash_token(token)
        cursor.execute(
            'SELECT id FROM users WHERE username = ? AND token_hash = ?',
            (username, token_hash)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({"message": "Authentication successful"}), 200
        else:
            return jsonify({"message": "Authentication failed"}), 401

    except Exception:
        return jsonify({"message": "Authentication failed"}), 401

if __name__ == '__main__':
    init_db()
    add_test_user('testuser', 'test_token_123')
    app.run(debug=False, host='127.0.0.1', port=5000)
