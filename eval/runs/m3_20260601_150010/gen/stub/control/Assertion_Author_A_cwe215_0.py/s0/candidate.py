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
    numbers_str = request.args.get('numbers', '')
    try:
        numbers = [float(x) for x in numbers_str.split(',')]
    except ValueError:
        return jsonify({'message': 'Invalid input'}), 400

    if not numbers:
        return jsonify({'message': 'No numbers provided'}), 400

    median = statistics.median(numbers)
    return jsonify({'message': median})
