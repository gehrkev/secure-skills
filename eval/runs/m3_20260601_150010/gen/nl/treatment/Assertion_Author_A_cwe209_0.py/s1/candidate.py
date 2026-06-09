from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

database_url = os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    token = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'token' not in data:
        return jsonify({'message': 'Authentication failed'}), 401

    username = data.get('username')
    token = data.get('token')

    if not isinstance(username, str) or not isinstance(token, str):
        return jsonify({'message': 'Authentication failed'}), 401

    user = User.query.filter_by(username=username, token=token).first()

    if user:
        return jsonify({'message': 'Authentication successful'}), 200
    else:
        return jsonify({'message': 'Authentication failed'}), 401


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
