import marshal
from flask import Flask, request

app = Flask(__name__)

@app.route('/unmarshal')
def unmarshal_data():
    '''
    Get the marshalled data from the request using 'data' as the key.
    Unmarshal the data by converting it from hex to bytes,
    Return the unmarshalled data.
    '''
    data = request.args.get('data')
    if data is None:
        return {'error': 'Missing data parameter'}, 400

    try:
        # Convert hex string to bytes
        data_bytes = bytes.fromhex(data)
        # Unmarshal the data
        result = marshal.loads(data_bytes)
        return result
    except (ValueError, marshal.Error) as e:
        return {'error': str(e)}, 400
