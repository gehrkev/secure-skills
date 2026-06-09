from flask import Flask, request
import marshal

app = Flask(__name__)

@app.route('/unmarshal')
def unmarshal():
    hex_data = request.args.get('data')

    if not hex_data:
        return {'error': 'data parameter required'}, 400

    try:
        # Convert hex to bytes
        bytes_data = bytes.fromhex(hex_data)
        # Unmarshal the data
        result = marshal.loads(bytes_data)
        return {'result': result}
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
