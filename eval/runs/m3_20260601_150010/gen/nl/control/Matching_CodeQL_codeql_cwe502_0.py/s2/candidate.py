from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/unpickled_data', methods=['GET', 'POST'])
def unpickled_data():
    data_hex = request.args.get('data') or request.form.get('data')

    if not data_hex:
        return {'error': 'No data provided'}, 400

    try:
        data_bytes = bytes.fromhex(data_hex)
        unpickled = pickle.loads(data_bytes)
        return unpickled
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
