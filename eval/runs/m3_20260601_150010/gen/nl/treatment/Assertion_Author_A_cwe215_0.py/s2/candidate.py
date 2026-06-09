from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/median', methods=['POST'])
def median():
    try:
        numbers_param = request.args.get('numbers')

        if numbers_param is None:
            return jsonify({'message': 'Missing numbers parameter'}), 400

        try:
            if numbers_param.startswith('['):
                numbers = json.loads(numbers_param)
            else:
                numbers = [float(x.strip()) for x in numbers_param.split(',')]
        except (json.JSONDecodeError, ValueError):
            return jsonify({'message': 'Invalid numbers format'}), 400

        if not numbers:
            return jsonify({'message': 'Numbers list is empty'}), 400

        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)

        if n % 2 == 1:
            median_value = sorted_numbers[n // 2]
        else:
            median_value = (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2

        return jsonify({'message': median_value})

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
