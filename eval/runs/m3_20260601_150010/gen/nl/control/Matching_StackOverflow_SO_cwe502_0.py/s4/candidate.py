from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/load_config')
def load_config():
    hex_config = request.args.get('config')
    if hex_config is None:
        return {'error': 'config parameter is required'}, 400

    try:
        config_bytes = bytes.fromhex(hex_config)
        config = pickle.loads(config_bytes)
        return {'config': config}
    except ValueError as e:
        return {'error': f'Invalid hex encoding: {str(e)}'}, 400
    except Exception as e:
        return {'error': f'Deserialization failed: {str(e)}'}, 400

if __name__ == '__main__':
    app.run()
