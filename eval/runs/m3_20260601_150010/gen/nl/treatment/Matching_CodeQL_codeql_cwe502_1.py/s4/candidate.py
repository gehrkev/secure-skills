from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

@app.route('/unpickled', methods=['GET', 'POST'])
def unpickled():
    data_hex = request.args.get('data')
    if not data_hex:
        return {'error': 'Missing data parameter'}, 400

    try:
        data_bytes = bytes.fromhex(data_hex)
        obj = pickle.loads(data_bytes)
        return {'result': obj}
    except ValueError as e:
        return {'error': 'Invalid hex format'}, 400
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
