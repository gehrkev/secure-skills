from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)


@app.route('/get_post', methods=['GET', 'POST'])
def get_post():
    title = request.args.get('title') or request.form.get('title')

    if not title:
        return jsonify({'error': 'Missing title parameter'}), 400

    try:
        post = Post.query.filter_by(title=title).first()

        if not post:
            return jsonify({'error': 'Post not found'}), 404

        return jsonify({'title': post.title, 'content': post.content}), 200

    except SQLAlchemyError:
        return jsonify({'error': 'Database error'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
