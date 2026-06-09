import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/unpickled')
def unpickled():
    data = request.args.get('data')
    if data is None:
        return jsonify({'error': 'data parameter is required'}), 400

    try:
        # Convert hex string to bytes
        byte_data = bytes.fromhex(data)
        # Deserialize the pickled object
        obj = pickle.loads(byte_data)
        return obj
    except ValueError:
        return jsonify({'error': 'Invalid hex format'}), 400
    except pickle.UnpicklingError as e:
        return jsonify({'error': f'Unpickling error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run()
