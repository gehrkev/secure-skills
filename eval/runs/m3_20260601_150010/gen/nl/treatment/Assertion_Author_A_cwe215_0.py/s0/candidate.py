from flask import Flask, request, jsonify
import statistics

app = Flask(__name__)

@app.route('/median', methods=['POST'])
def median():
    numbers_str = request.args.get('numbers')

    if not numbers_str:
        return jsonify({'message': 'Error: no numbers parameter provided'}), 400

    try:
        numbers = [float(x.strip()) for x in numbers_str.split(',')]

        if not numbers:
            return jsonify({'message': 'Error: empty numbers list'}), 400

        result = statistics.median(numbers)
        return jsonify({'message': result})

    except ValueError:
        return jsonify({'message': 'Error: invalid number format'}), 400

if __name__ == '__main__':
    app.run(debug=True)
