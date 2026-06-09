from flask import Flask, request
import marshal

app = Flask(__name__)

@app.route('/unmarshal', methods=['GET', 'POST'])
def unmarshal_endpoint():
    data_hex = request.args.get('data')
    if not data_hex:
        return {'error': 'data parameter required'}, 400

    try:
        data_bytes = bytes.fromhex(data_hex)
        result = marshal.loads(data_bytes)
        return {'result': result}
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
