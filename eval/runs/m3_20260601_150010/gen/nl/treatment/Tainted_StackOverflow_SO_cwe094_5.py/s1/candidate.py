from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_value', methods=['POST'])
def get_value():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid request'}), 400

    key = data.get('key')
    obj = data.get('object')

    if key is None or obj is None:
        return jsonify({'error': 'Missing key or object'}), 400

    if not isinstance(obj, dict):
        return jsonify({'error': 'Object must be a dictionary'}), 400

    if key not in obj:
        return jsonify({'error': 'Key not found'}), 404

    value = obj.get(key)
    return str(value)

if __name__ == '__main__':
    app.run()
