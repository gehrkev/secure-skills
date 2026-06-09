from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, token TEXT)''')
    try:
        c.execute("INSERT INTO users (username, token) VALUES (?, ?)", ("user1", "token123"))
        c.execute("INSERT INTO users (username, token) VALUES (?, ?)", ("user2", "token456"))
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'token' not in data:
        return jsonify({"message": "Authentication failed"}), 400

    username = data['username']
    token = data['token']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND token = ?", (username, token))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Authentication successful"}), 200
    else:
        return jsonify({"message": "Authentication failed"}), 401

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
