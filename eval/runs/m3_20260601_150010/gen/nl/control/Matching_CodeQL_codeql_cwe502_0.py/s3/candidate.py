from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/unpickled_data', methods=['GET', 'POST'])
def unpickled_data():
    hex_data = request.args.get('data') or request.form.get('data')

    if not hex_data:
        json_data = request.get_json()
        if json_data:
            hex_data = json_data.get('data')

    bytes_data = bytes.fromhex(hex_data)
    unpickled = pickle.loads(bytes_data)

    return unpickled

if __name__ == '__main__':
    app.run()
