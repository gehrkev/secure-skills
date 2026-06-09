from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/load_config')
def load_config():
    config_hex = request.args.get('config')
    if config_hex is None:
        return {'error': 'config parameter is required'}, 400

    try:
        config_bytes = bytes.fromhex(config_hex)
        config = pickle.loads(config_bytes)
        return {'config': config}
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
