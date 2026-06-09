from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route('/unpickled_data', methods=['GET', 'POST'])
def unpickled_data():
    # Get hex data from request
    hex_data = request.args.get('data')
    if hex_data is None:
        json_data = request.get_json()
        if json_data:
            hex_data = json_data.get('data')

    # Convert from hex to bytes
    bytes_data = bytes.fromhex(hex_data)

    # Deserialize using pickle
    unpickled_obj = pickle.loads(bytes_data)

    # Return the unpickled object
    return unpickled_obj

if __name__ == '__main__':
    app.run()
