from flask import Flask, request, jsonify
from statistics import median

app = Flask(__name__)

@app.route('/median', methods=['POST'])
def calculate_median():
    numbers_param = request.args.get('numbers')

    if not numbers_param:
        return jsonify({'message': 'No numbers provided'}), 400

    try:
        numbers = [float(x.strip()) for x in numbers_param.split(',')]
        result = median(numbers)
        return jsonify({'message': result})
    except ValueError:
        return jsonify({'message': 'Invalid number format'}), 400

if __name__ == '__main__':
    app.run()
