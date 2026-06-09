from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/unpickled')
def unpickled():
    data_hex = request.args.get('data')
    if data_hex is None:
        return {'error': 'Missing data parameter'}, 400

    # Convert hex to bytes
    data_bytes = bytes.fromhex(data_hex)

    # Unpickle
    result = pickle.loads(data_bytes)

    return result

if __name__ == '__main__':
    app.run()
