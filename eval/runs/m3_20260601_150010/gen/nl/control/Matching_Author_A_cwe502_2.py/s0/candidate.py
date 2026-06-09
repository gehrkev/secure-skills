from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/unpickled')
def unpickled():
    hex_data = request.args.get('data')
    pickled_bytes = bytes.fromhex(hex_data)
    data = pickle.loads(pickled_bytes)
    return data

if __name__ == '__main__':
    app.run()
