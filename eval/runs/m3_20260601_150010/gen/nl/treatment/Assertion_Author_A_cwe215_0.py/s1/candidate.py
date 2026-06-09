from flask import Flask, request, jsonify
import statistics

app = Flask(__name__)

@app.route('/median', methods=['POST'])
def median():
    numbers_str = request.args.get('numbers', '')

    try:
        # Parse comma or space-separated numbers
        if ',' in numbers_str:
            numbers = [float(x.strip()) for x in numbers_str.split(',')]
        else:
            numbers = [float(x.strip()) for x in numbers_str.split()]

        # Validate we have numbers (CWE-369: Divide By Zero prevention)
        if not numbers:
            return jsonify({'message': 'Error: no numbers provided'}), 400

        result = statistics.median(numbers)
        return jsonify({'message': result})

    except ValueError:
        return jsonify({'message': 'Error: invalid number format'}), 400

if __name__ == '__main__':
    app.run()
