from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/load_config')
def load_config():
    config_hex = request.args.get('config')
    if not config_hex:
        return {'error': 'config parameter is required'}, 400

    try:
        config_bytes = bytes.fromhex(config_hex)
        config = pickle.loads(config_bytes)
        return {'config': config}, 200
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
