from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/unpickled_data', methods=['GET', 'POST'])
def unpickled_data():
    hex_data = request.args.get('data') or request.form.get('data')
    bytes_data = bytes.fromhex(hex_data)
    unpickled_obj = pickle.loads(bytes_data)
    return unpickled_obj

if __name__ == '__main__':
    app.run()
