from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    token = db.Column(db.String(255), nullable=False)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'token' not in data:
        return jsonify({"message": "Unauthorized"}), 401

    username = data.get('username')
    token = data.get('token')

    user = User.query.filter_by(username=username, token=token).first()

    if user:
        return jsonify({"message": "Authorized"}), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
