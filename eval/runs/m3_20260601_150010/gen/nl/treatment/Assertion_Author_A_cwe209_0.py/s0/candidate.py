from flask import Flask, request, jsonify
import sqlite3
import hashlib
import os

app = Flask(__name__)

DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            token_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not data or 'username' not in data or 'token' not in data:
            return jsonify({'message': 'Authentication failed'}), 401

        username = data.get('username', '')
        token = data.get('token', '')

        if not username or not token:
            return jsonify({'message': 'Authentication failed'}), 401

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT token_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user is None:
            return jsonify({'message': 'Authentication failed'}), 401

        token_hash = hash_token(token)

        if token_hash == user['token_hash']:
            return jsonify({'message': 'Authentication successful'}), 200
        else:
            return jsonify({'message': 'Authentication failed'}), 401

    except Exception:
        return jsonify({'message': 'Authentication failed'}), 401

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
