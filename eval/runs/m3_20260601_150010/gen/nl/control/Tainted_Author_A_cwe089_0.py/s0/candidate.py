from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)

@app.route('/get_post', methods=['GET'])
def get_post():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'title parameter is required'}), 400

    post = Post.query.filter_by(title=title).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    return jsonify({'content': post.content}), 200

if __name__ == '__main__':
    app.run(debug=True)
