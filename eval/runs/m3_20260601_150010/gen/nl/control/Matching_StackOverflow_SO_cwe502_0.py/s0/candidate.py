from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/load_config')
def load_config():
    config = request.args.get('config')
    if not config:
        return {'error': 'config parameter required'}, 400

    try:
        config_bytes = bytes.fromhex(config)
        data = pickle.loads(config_bytes)
        return {'data': str(data)}
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
