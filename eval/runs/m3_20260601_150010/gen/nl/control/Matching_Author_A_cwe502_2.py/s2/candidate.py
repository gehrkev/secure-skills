from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/unpickled', methods=['GET'])
def unpickled():
    data = request.args.get('data')
    bytes_data = bytes.fromhex(data)
    deserialized_data = pickle.loads(bytes_data)
    return deserialized_data

if __name__ == '__main__':
    app.run()
