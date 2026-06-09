from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_value', methods=['POST'])
def get_value():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        key = data.get('key')
        obj = data.get('object')

        if not isinstance(key, str):
            return jsonify({'error': 'Key must be a string'}), 400

        if not isinstance(obj, dict):
            return jsonify({'error': 'Object must be a dictionary'}), 400

        if key not in obj:
            return jsonify({'error': 'Key not found in object'}), 404

        value = str(obj[key])
        return jsonify({'value': value})

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run()
