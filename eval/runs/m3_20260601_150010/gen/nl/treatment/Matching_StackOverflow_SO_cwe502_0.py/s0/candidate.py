from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/load_config')
def load_config():
    config_hex = request.args.get('config')
    if not config_hex:
        return {'error': 'config parameter missing'}, 400

    try:
        config_bytes = bytes.fromhex(config_hex)
        config = pickle.loads(config_bytes)
        return {'config': config}
    except ValueError:
        return {'error': 'invalid hex encoding'}, 400
    except Exception:
        return {'error': 'deserialization failed'}, 400
