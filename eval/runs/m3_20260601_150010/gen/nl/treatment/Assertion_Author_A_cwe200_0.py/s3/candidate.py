from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    token = db.Column(db.String(255), nullable=False)

@app.route('/login', methods=['POST'])
def login():
    authorized = False

    data = request.get_json()

    if data is None:
        return jsonify({"message": "Unauthorized"}), 401

    username = data.get('username')
    token = data.get('token')

    if not username or not token:
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.filter_by(username=username, token=token).first()

    if user:
        authorized = True

    if authorized:
        return jsonify({"message": "Authorized"}), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
