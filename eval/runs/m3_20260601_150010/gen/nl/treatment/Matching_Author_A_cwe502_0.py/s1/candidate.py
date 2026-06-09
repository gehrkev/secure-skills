from flask import Flask, request, jsonify
import marshal

app = Flask(__name__)

@app.route('/unmarshal', methods=['GET', 'POST'])
def unmarshal():
    try:
        hex_data = request.args.get('data') or request.form.get('data')

        if not hex_data:
            return jsonify({'error': 'Missing data parameter'}), 400

        # Convert hex to bytes
        try:
            data_bytes = bytes.fromhex(hex_data)
        except ValueError:
            return jsonify({'error': 'Invalid hex encoding'}), 400

        # Unmarshal the data
        result = marshal.loads(data_bytes)

        # Try to JSON encode the result, fall back to string representation
        try:
            return jsonify({'result': result})
        except TypeError:
            return jsonify({'result': repr(result)})

    except Exception as e:
        return jsonify({'error': 'Failed to unmarshal data'}), 400

if __name__ == '__main__':
    app.run()
