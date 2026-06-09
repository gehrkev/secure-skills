from flask import Flask, request, jsonify
from statistics import median

app = Flask(__name__)

@app.route('/median', methods=['POST'])
def calculate_median():
    numbers_param = request.args.get('numbers', '')
    try:
        numbers = [float(x.strip()) for x in numbers_param.split(',') if x.strip()]
        if not numbers:
            return jsonify({'message': 'No numbers provided'}), 400
        result = median(numbers)
        return jsonify({'message': result})
    except ValueError:
        return jsonify({'message': 'Invalid number format'}), 400

if __name__ == '__main__':
    app.run()
