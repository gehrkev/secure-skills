from flask import Flask, request, jsonify
from statistics import median

app = Flask(__name__)

@app.route('/median', methods=['POST'])
def calculate_median():
    # Get the 'numbers' query parameter
    numbers_param = request.args.get('numbers', '')

    try:
        # Validate that parameter is provided and not empty
        if not numbers_param:
            return jsonify({'message': 'Error: numbers parameter is required'}), 400

        # Parse numbers from the parameter
        # Handle both comma-separated and space-separated formats
        numbers = [float(x.strip()) for x in numbers_param.replace(',', ' ').split() if x.strip()]

        # CWE-369 mitigation: check for empty list to prevent divide by zero issues
        if not numbers:
            return jsonify({'message': 'Error: At least one number is required'}), 400

        # Calculate median
        result = median(numbers)
        return jsonify({'message': result})

    except ValueError:
        # Handle invalid number format
        return jsonify({'message': 'Error: Invalid number format'}), 400

if __name__ == '__main__':
    app.run(debug=False)
