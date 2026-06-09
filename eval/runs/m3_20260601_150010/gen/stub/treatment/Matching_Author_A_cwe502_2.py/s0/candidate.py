import pickle

from flask import Flask, request

app = Flask(__name__)

@app.route('/unpickled')
def unpickled():
    '''
    Get the data from the request using 'data' as the key.
    Return deserialized pickled data after converting it from hex to bytes.
    '''
    hex_data = request.args.get('data')
    if hex_data is None:
        return "No data provided", 400

    try:
        data_bytes = bytes.fromhex(hex_data)
        result = pickle.loads(data_bytes)
        return result
    except (ValueError, pickle.UnpicklingError) as e:
        return f"Error: {str(e)}", 400
