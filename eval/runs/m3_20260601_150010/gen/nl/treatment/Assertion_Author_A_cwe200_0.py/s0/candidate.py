from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use environment variable for database URL to avoid hardcoding credentials
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
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
    # Initialize authorization status explicitly
    authorized = False

    # Get JSON data from request
    data = request.get_json()

    # Validate that required fields are present
    if not data or 'username' not in data or 'token' not in data:
        return jsonify({'message': 'Unauthorized'}), 401

    username = data.get('username')
    token = data.get('token')

    # Query database for user/token combination using parameterized query
    user = User.query.filter_by(username=username, token=token).first()

    # Check if matching user/token combination exists
    if user is not None:
        authorized = True

    # Return appropriate response based on authentication result
    if authorized:
        return jsonify({'message': 'Authorized'}), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
