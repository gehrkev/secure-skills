from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_average_score', methods=['POST', 'GET'])
def get_average_score():
    try:
        # Extract from request (support both JSON and query parameters)
        if request.is_json:
            data = request.get_json()
            total_score = data.get('total_score')
            total_count = data.get('total_count')
        else:
            total_score = request.args.get('total_score')
            total_count = request.args.get('total_count')

        # Validate that values exist
        if total_score is None or total_count is None:
            return jsonify({'error': 'Missing total_score or total_count'}), 400

        # Convert to numbers and validate
        try:
            total_score = float(total_score)
            total_count = float(total_count)
        except (ValueError, TypeError):
            return jsonify({'error': 'total_score and total_count must be numbers'}), 400

        # Prevent divide by zero (CWE-369)
        if total_count == 0:
            return jsonify({'error': 'total_count cannot be zero'}), 400

        # Calculate and return average
        average_score = total_score / total_count
        return jsonify({'average_score': average_score})

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
