from flask import Flask, request
import marshal

app = Flask(__name__)

@app.route('/unmarshal', methods=['GET', 'POST'])
def unmarshal_data():
    data = request.args.get('data')
    if not data:
        return {'error': 'Missing data parameter'}, 400

    try:
        byte_data = bytes.fromhex(data)
        result = marshal.loads(byte_data)
        return result
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
