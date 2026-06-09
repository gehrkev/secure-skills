from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'users.db'

def init_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE users
                 (id INTEGER PRIMARY KEY, username TEXT, token TEXT)''')
    c.execute("INSERT INTO users (username, token) VALUES (?, ?)", ('user1', 'token123'))
    c.execute("INSERT INTO users (username, token) VALUES (?, ?)", ('user2', 'token456'))
    conn.commit()
    return conn

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"message": "Unauthorized"}), 401

    username = data.get('username')
    token = data.get('token')

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND token = ?', (username, token))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Authorized"}), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
