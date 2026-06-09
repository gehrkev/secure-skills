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
        return {'error': 'No data provided'}, 400

    try:
        data_bytes = bytes.fromhex(data)
        result = marshal.loads(data_bytes)
        return result
    except (ValueError, EOFError) as e:
        return {'error': f'Failed to unmarshal data: {str(e)}'}, 400
