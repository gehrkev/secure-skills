from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_average_score', methods=['GET', 'POST'])
def get_average_score():
    # Extract total_score and total_count from request
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        total_score = data.get('total_score')
        total_count = data.get('total_count')
    else:
        total_score = request.args.get('total_score')
        total_count = request.args.get('total_count')

    # Validate that both parameters are provided
    if total_score is None or total_count is None:
        return jsonify({'error': 'Missing total_score or total_count'}), 400

    # Convert to numbers
    try:
        total_score = float(total_score)
        total_count = float(total_count)
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input: total_score and total_count must be numbers'}), 400

    # Check for division by zero
    if total_count == 0:
        return jsonify({'error': 'total_count cannot be zero'}), 400

    # Calculate and return average
    average_score = total_score / total_count
    return jsonify({'average_score': average_score})

if __name__ == '__main__':
    app.run(debug=True)
