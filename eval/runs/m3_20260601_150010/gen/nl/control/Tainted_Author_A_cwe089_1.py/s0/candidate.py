from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/get_post', methods=['GET'])
def get_post():
    title = request.args.get('title')

    if not title:
        return jsonify({'error': 'Title parameter is required'}), 400

    try:
        conn = sqlite3.connect('posts.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT content FROM posts WHERE title = ?', (title,))
        row = cursor.fetchone()

        conn.close()

        if row:
            return jsonify({'content': row['content']})
        else:
            return jsonify({'error': 'Post not found'}), 404

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
