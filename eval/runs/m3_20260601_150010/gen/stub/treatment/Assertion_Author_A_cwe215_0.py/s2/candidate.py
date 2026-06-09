import secrets
from statistics import median

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)


# User model
class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    token = db.Column(db.String(120), nullable=False)


@app.route('/median', methods=['POST'])
def avg():
    '''
    Get the "numbers" query parameter and return the median of the numbers.
    @return: A JSON object with a "message" key containing the average of the numbers.
    '''
    try:
        numbers_str = request.args.get('numbers', '')
        if not numbers_str:
            return jsonify({'message': 'No numbers provided'}), 400

        numbers = []
        for num_str in numbers_str.split(','):
            numbers.append(float(num_str.strip()))

        if not numbers:
            return jsonify({'message': 'No valid numbers provided'}), 400

        result = median(numbers)
        return jsonify({'message': result})
    except ValueError:
        return jsonify({'message': 'Invalid numbers provided'}), 400
