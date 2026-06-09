from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_average_score', methods=['GET', 'POST'])
def get_average_score():
    if request.method == 'GET':
        total_score = request.args.get('total_score')
        total_count = request.args.get('total_count')
    else:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        total_score = data.get('total_score')
        total_count = data.get('total_count')

    if total_score is None or total_count is None:
        return jsonify({'error': 'Missing required parameters: total_score and total_count'}), 400

    try:
        total_score = float(total_score)
        total_count = float(total_count)
    except (ValueError, TypeError):
        return jsonify({'error': 'Parameters must be valid numbers'}), 400

    if total_count == 0:
        return jsonify({'error': 'total_count cannot be zero'}), 400

    average_score = total_score / total_count

    return jsonify({'average_score': average_score})

if __name__ == '__main__':
    app.run(debug=True)
