from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/unpickled')
def unpickled():
    data_hex = request.args.get('data')
    data_bytes = bytes.fromhex(data_hex)
    result = pickle.loads(data_bytes)
    return result

if __name__ == '__main__':
    app.run()
