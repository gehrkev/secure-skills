from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_average_score', methods=['GET', 'POST'])
def get_average_score():
    if request.method == 'GET':
        total_score = request.args.get('total_score')
        total_count = request.args.get('total_count')
    else:
        data = request.get_json() or request.form
        total_score = data.get('total_score')
        total_count = data.get('total_count')

    if total_score is None or total_count is None:
        return jsonify({'error': 'Missing total_score or total_count'}), 400

    try:
        total_score = float(total_score)
        total_count = float(total_count)

        if total_count == 0:
            return jsonify({'error': 'total_count cannot be zero'}), 400

        average_score = total_score / total_count
        return jsonify({'average_score': average_score})
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid total_score or total_count'}), 400

if __name__ == '__main__':
    app.run()
