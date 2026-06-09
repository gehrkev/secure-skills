from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_value', methods=['POST'])
def get_value():
    try:
        data = request.get_json()

        if not data or 'key' not in data or 'object' not in data:
            return jsonify({'error': 'Missing key or object'}), 400

        key = data.get('key')
        obj = data.get('object')

        if not isinstance(obj, dict):
            return jsonify({'error': 'Object must be a dictionary'}), 400

        value = obj.get(key)
        return str(value)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
