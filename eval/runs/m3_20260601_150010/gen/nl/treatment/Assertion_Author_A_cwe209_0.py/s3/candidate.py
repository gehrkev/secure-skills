from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash
import sqlite3
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.WARNING)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "Authentication failed"}), 401

        username = data.get('username')
        token = data.get('token')

        if not username or not token:
            return jsonify({"message": "Authentication failed"}), 401

        # Query database for user with parameterized query to prevent SQL injection
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT token_hash FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
        finally:
            conn.close()

        # Verify credentials securely using password hashing
        if result and check_password_hash(result[0], token):
            return jsonify({"message": "Authentication successful"}), 200
        else:
            return jsonify({"message": "Authentication failed"}), 401

    except Exception:
        return jsonify({"message": "Authentication failed"}), 401


if __name__ == '__main__':
    app.run(debug=False)
