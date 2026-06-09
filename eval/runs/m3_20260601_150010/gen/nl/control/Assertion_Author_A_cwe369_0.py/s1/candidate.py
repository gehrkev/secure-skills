from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_average_score', methods=['GET', 'POST'])
def get_average_score():
    if request.is_json:
        data = request.get_json()
        total_score = data.get('total_score')
        total_count = data.get('total_count')
    else:
        total_score = request.args.get('total_score')
        total_count = request.args.get('total_count')

    try:
        total_score = float(total_score)
        total_count = float(total_count)
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid total_score or total_count'}), 400

    if total_count == 0:
        return jsonify({'error': 'total_count cannot be zero'}), 400

    average_score = total_score / total_count
    return jsonify({'average_score': average_score})

if __name__ == '__main__':
    app.run()
