from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database with sample users
def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            token TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT INTO users VALUES ('admin', 'secret123')")
    cursor.execute("INSERT INTO users VALUES ('user', 'token456')")
    conn.commit()
    return conn

db = init_db()

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        token = data.get('token')

        if not username or not token:
            return jsonify({"message": "Authentication failed"}), 401

        cursor = db.cursor()
        cursor.execute('SELECT token FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()

        if result and result[0] == token:
            return jsonify({"message": "Authentication successful"}), 200
        else:
            return jsonify({"message": "Authentication failed"}), 401
    except Exception:
        return jsonify({"message": "Authentication failed"}), 401

if __name__ == '__main__':
    app.run(debug=True)
