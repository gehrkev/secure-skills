from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_value', methods=['POST'])
def get_value():
    # Get JSON data from request
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'Request must be JSON'}), 400

    key = data.get('key')
    obj = data.get('object')

    # Validate inputs
    if key is None:
        return jsonify({'error': 'Missing key parameter'}), 400

    if obj is None:
        return jsonify({'error': 'Missing object parameter'}), 400

    # Ensure object is a dictionary (safe type)
    if not isinstance(obj, dict):
        return jsonify({'error': 'Object parameter must be a dictionary'}), 400

    # Safely retrieve value from object
    if key not in obj:
        return jsonify({'error': f'Key "{key}" not found in object'}), 404

    value = obj[key]

    # Return value as string
    return str(value)

if __name__ == '__main__':
    app.run(debug=True)
