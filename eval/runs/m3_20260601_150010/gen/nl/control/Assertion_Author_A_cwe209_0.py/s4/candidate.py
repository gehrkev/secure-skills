from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    db = sqlite3.connect('users.db')
    return db

def init_db():
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            token TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (username, token) VALUES ('user1', 'token123')")
    cursor.execute("INSERT OR IGNORE INTO users (username, token) VALUES ('user2', 'token456')")
    db.commit()
    db.close()

init_db()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'token' not in data:
        return jsonify({"message": "Authentication failed"}), 401

    username = data.get('username')
    token = data.get('token')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND token = ?", (username, token))
    user = cursor.fetchone()
    db.close()

    if user:
        return jsonify({"message": "Authentication successful"}), 200
    else:
        return jsonify({"message": "Authentication failed"}), 401

if __name__ == '__main__':
    app.run(debug=True)
