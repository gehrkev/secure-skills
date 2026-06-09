from flask import Flask, request, jsonify
import statistics

app = Flask(__name__)

@app.route('/median', methods=['POST'])
def median():
    numbers_str = request.args.get('numbers')

    if not numbers_str:
        return jsonify({'message': 'No numbers provided'}), 400

    try:
        numbers = [float(x) for x in numbers_str.split(',')]
        result = statistics.median(numbers)
        return jsonify({'message': result})
    except ValueError:
        return jsonify({'message': 'Invalid numbers'}), 400

if __name__ == '__main__':
    app.run()
