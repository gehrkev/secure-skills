from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_average_score', methods=['POST', 'GET'])
def get_average_score():
    try:
        if request.method == 'POST':
            data = request.get_json()
        else:
            data = request.args.to_dict()

        total_score = data.get('total_score')
        total_count = data.get('total_count')

        if total_score is None or total_count is None:
            return jsonify({'error': 'Missing required parameters: total_score and total_count'}), 400

        total_score = float(total_score)
        total_count = float(total_count)

        if total_count == 0:
            return jsonify({'error': 'total_count cannot be zero'}), 400

        average_score = total_score / total_count

        return jsonify({'average_score': average_score}), 200

    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input: total_score and total_count must be numeric'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
