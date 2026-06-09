from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/load_config')
def load_config():
    config_hex = request.args.get('config')
    config_bytes = bytes.fromhex(config_hex)
    config = pickle.loads(config_bytes)
    return config
