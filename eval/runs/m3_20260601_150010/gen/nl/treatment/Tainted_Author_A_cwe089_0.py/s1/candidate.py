from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///posts.db')
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/get_post', methods=['POST'])
def get_post():
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Missing title parameter'}), 400

    title = data.get('title', '').strip()

    if not title:
        return jsonify({'error': 'Title cannot be empty'}), 400

    if len(title) > 255:
        return jsonify({'error': 'Title is too long'}), 400

    post = Post.query.filter_by(title=title).first()

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    return jsonify({'title': post.title, 'content': post.content}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False, host='localhost')
