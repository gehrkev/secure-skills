import marshal
from flask import Flask, request

app = Flask(__name__)

@app.route('/unmarshal_config', methods=['GET', 'POST'])
def unmarshal_config_data():
    '''
    Get the config data from the request using 'config' as the key.
    Unmarshal the data after decoding it from hex.
    Return the unmarshalled data.
    '''
    config_hex = request.values.get('config')
    config_bytes = bytes.fromhex(config_hex)
    config_data = marshal.loads(config_bytes)
    return config_data
