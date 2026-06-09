from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_average_score', methods=['GET', 'POST'])
def get_average_score():
    # Extract from JSON body or query parameters
    if request.is_json:
        data = request.get_json()
    else:
        data = request.args.to_dict()

    total_score = data.get('total_score')
    total_count = data.get('total_count')

    # Validate that parameters exist
    if total_score is None or total_count is None:
        return jsonify({'error': 'Missing required parameters: total_score and total_count'}), 400

    # Convert to numbers and validate
    try:
        total_score = float(total_score)
        total_count = float(total_count)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input: total_score and total_count must be numbers'}), 400

    # Check for divide by zero (CWE-369)
    if total_count == 0:
        return jsonify({'error': 'total_count cannot be zero'}), 400

    # Calculate and return average
    average_score = total_score / total_count
    return jsonify({'average_score': average_score})

if __name__ == '__main__':
    app.run(debug=True)
