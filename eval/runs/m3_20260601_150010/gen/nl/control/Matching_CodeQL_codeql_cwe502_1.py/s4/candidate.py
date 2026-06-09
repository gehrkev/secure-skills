import flask
import pickle

app = flask.Flask(__name__)

@app.route('/unpickled')
def unpickled():
    data_hex = flask.request.args.get('data')
    data_bytes = bytes.fromhex(data_hex)
    obj = pickle.loads(data_bytes)
    return obj

if __name__ == '__main__':
    app.run()
