from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('posts.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/get_post', methods=['GET'])
def get_post():
    title = request.args.get('title')

    if not title:
        return jsonify({'error': 'Title parameter is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Use parameterized query to prevent SQL injection (CWE-89)
    cursor.execute('SELECT content FROM posts WHERE title = ?', (title,))
    post = cursor.fetchone()
    conn.close()

    if post is None:
        return jsonify({'error': 'Post not found'}), 404

    return jsonify({'content': post['content']})

if __name__ == '__main__':
    app.run(debug=True)
