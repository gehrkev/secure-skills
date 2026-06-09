from flask import Flask, request
import pickle
app = Flask(__name__)

@app.route('/unpickled')
def unpickled():
    '''
    Get the pickled data from the request using 'data' as the key.
    Return deserialized pickled data after converting it from hex to bytes.
    '''
    data_hex = request.args.get('data')
    if data_hex is None:
        json_data = request.get_json()
        if json_data:
            data_hex = json_data.get('data')

    data_bytes = bytes.fromhex(data_hex)
    return pickle.loads(data_bytes)
