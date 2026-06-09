from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    """Initialize the database with sample users."""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, token TEXT)''')
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", ('user1', 'token123'))
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", ('user2', 'token456'))
    conn.commit()
    conn.close()

init_db()

@app.route('/login', methods=['POST'])
def login():
    """Login endpoint that verifies username and token against the database."""
    data = request.get_json()

    if not data or 'username' not in data or 'token' not in data:
        return jsonify({"message": "Authentication failed"}), 401

    username = data.get('username')
    token = data.get('token')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT token FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result and result[0] == token:
        return jsonify({"message": "Authentication successful"}), 200
    else:
        return jsonify({"message": "Authentication failed"}), 401

if __name__ == '__main__':
    app.run(debug=True)
