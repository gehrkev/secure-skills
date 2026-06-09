from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/unpickled')
def unpickled():
    data = request.args.get('data')
    bytes_data = bytes.fromhex(data)
    result = pickle.loads(bytes_data)
    return result

if __name__ == '__main__':
    app.run()
