from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                token TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    authorized = False

    try:
        data = request.get_json()

        if data is None:
            return jsonify({'message': 'Unauthorized'}), 401

        username = data.get('username')
        token = data.get('token')

        if not username or not token:
            return jsonify({'message': 'Unauthorized'}), 401

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE username = ? AND token = ?',
            (username, token)
        )
        user = cursor.fetchone()
        conn.close()

        if user is not None:
            authorized = True

    except Exception:
        authorized = False

    if authorized:
        return jsonify({'message': 'Authorized'}), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 401

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
