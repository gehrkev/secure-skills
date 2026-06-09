import flask
import pickle
import binascii

app = flask.Flask(__name__)

@app.route('/unpickled_data', methods=['POST', 'GET'])
def unpickled_data():
    hex_data = flask.request.args.get('data') or flask.request.form.get('data')

    if not hex_data:
        return {'error': 'Missing data parameter'}, 400

    try:
        data_bytes = binascii.unhexlify(hex_data)
        result = pickle.loads(data_bytes)
        return result
    except (binascii.Error, pickle.UnpicklingError) as e:
        return {'error': 'Invalid data'}, 400
