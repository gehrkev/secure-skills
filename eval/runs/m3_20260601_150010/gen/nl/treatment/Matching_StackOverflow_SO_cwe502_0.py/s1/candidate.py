from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/load_config', methods=['GET', 'POST'])
def load_config():
    config_hex = request.args.get('config') or request.form.get('config')

    if not config_hex:
        return {'error': 'Missing config parameter'}, 400

    try:
        config_bytes = bytes.fromhex(config_hex)
        config = pickle.loads(config_bytes)
        return {'config': config}
    except ValueError:
        return {'error': 'Invalid hex encoding'}, 400
    except Exception:
        return {'error': 'Failed to deserialize config'}, 400
