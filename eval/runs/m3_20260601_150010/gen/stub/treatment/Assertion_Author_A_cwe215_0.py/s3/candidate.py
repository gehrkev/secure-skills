import secrets
import statistics

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
        numbers_param = request.args.get('numbers')
        if not numbers_param:
            return jsonify({'message': 'numbers parameter is required'}), 400

        numbers = []
        for num_str in numbers_param.split(','):
            try:
                numbers.append(float(num_str.strip()))
            except ValueError:
                return jsonify({'message': 'Invalid number format'}), 400

        if not numbers:
            return jsonify({'message': 'No numbers provided'}), 400

        median = statistics.median(numbers)
        return jsonify({'message': median})
    except Exception as e:
        return jsonify({'message': 'Error processing request'}), 500
