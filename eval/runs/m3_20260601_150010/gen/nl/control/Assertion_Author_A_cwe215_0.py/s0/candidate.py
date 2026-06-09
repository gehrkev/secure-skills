from flask import Flask, request, jsonify
import statistics

app = Flask(__name__)

@app.route('/median', methods=['POST'])
def median():
    numbers_str = request.args.get('numbers', '')

    try:
        # Parse numbers (handle comma or space separated)
        if ',' in numbers_str:
            numbers = [float(x.strip()) for x in numbers_str.split(',')]
        else:
            numbers = [float(x.strip()) for x in numbers_str.split()]

        result = statistics.median(numbers)
        return jsonify({'message': result})
    except:
        return jsonify({'message': 'Error calculating median'}), 400

if __name__ == '__main__':
    app.run(debug=True)
