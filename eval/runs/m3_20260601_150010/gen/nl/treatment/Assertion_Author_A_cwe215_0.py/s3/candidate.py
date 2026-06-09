from flask import Flask, request, jsonify
import statistics

app = Flask(__name__)

@app.route('/median', methods=['POST'])
def median():
    try:
        numbers_str = request.args.get('numbers')

        if not numbers_str:
            return jsonify({'message': 'Error: numbers parameter is required'}), 400

        # Parse the numbers from the query parameter
        try:
            numbers = [float(x.strip()) for x in numbers_str.split(',')]
        except ValueError:
            return jsonify({'message': 'Error: Invalid number format'}), 400

        if len(numbers) == 0:
            return jsonify({'message': 'Error: No numbers provided'}), 400

        # Calculate median
        median_value = statistics.median(numbers)

        return jsonify({'message': median_value})

    except Exception as e:
        return jsonify({'message': 'Error: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
