import secrets
import statistics
import json

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
    numbers_param = request.args.get('numbers')
    if not numbers_param:
        return jsonify({'message': 'numbers parameter is required'}), 400

    try:
        # Try to parse as JSON array first
        if numbers_param.startswith('['):
            numbers = json.loads(numbers_param)
        else:
            # Try comma-separated or space-separated
            if ',' in numbers_param:
                numbers = [float(x.strip()) for x in numbers_param.split(',')]
            else:
                numbers = [float(x.strip()) for x in numbers_param.split()]

        if not numbers:
            return jsonify({'message': 'numbers list is empty'}), 400

        median = statistics.median(numbers)
        return jsonify({'message': median})
    except (ValueError, json.JSONDecodeError):
        return jsonify({'message': 'Invalid numbers provided'}), 400
