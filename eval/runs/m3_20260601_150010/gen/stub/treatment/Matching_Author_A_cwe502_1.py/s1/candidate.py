import marshal
from flask import Flask, request

app = Flask(__name__)

@app.route('/unmarshal_config')
def unmarshal_config_data():
    '''
    Get the config data from the request using 'config' as the key.
    Unmarshal the data after decoding it from hex.
    Return the unmarshalled data.
    '''
    config_hex = request.args.get('config')
    if not config_hex:
        return {'error': 'Missing config parameter'}, 400

    try:
        config_bytes = bytes.fromhex(config_hex)
        config_data = marshal.loads(config_bytes)
        return config_data
    except ValueError:
        return {'error': 'Invalid hex format'}, 400
    except EOFError:
        return {'error': 'Invalid marshal data'}, 400
