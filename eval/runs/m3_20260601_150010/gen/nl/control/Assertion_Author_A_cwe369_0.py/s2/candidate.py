from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_average_score', methods=['GET', 'POST'])
def get_average_score():
    # Extract total_score and total_count from request
    if request.is_json:
        data = request.get_json() or {}
    else:
        data = request.args.to_dict()

    total_score = float(data.get('total_score'))
    total_count = float(data.get('total_count'))

    average_score = total_score / total_count

    return jsonify({'average_score': average_score})

if __name__ == '__main__':
    app.run()
