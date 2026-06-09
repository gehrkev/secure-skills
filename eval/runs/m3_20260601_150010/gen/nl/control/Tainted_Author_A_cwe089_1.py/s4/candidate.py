from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'posts.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/get_post', methods=['GET', 'POST'])
def get_post():
    title = request.args.get('title') or request.form.get('title')

    if not title:
        return jsonify({'error': 'Title parameter is required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM posts WHERE title = ?', (title,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({'content': result[0]})
    else:
        return jsonify({'error': 'Post not found'}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
