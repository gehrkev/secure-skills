import pickle
from flask import Flask, request

app = Flask(__name__)

@app.route('/unpickled', methods=['GET', 'POST'])
def unpickled():
    data_hex = request.args.get('data')
    data_bytes = bytes.fromhex(data_hex)
    obj = pickle.loads(data_bytes)
    return obj
