from flask import Flask, request
import marshal

app = Flask(__name__)

@app.route('/unmarshal', methods=['GET', 'POST'])
def unmarshal():
    data_hex = request.args.get('data')
    if not data_hex and request.method == 'POST':
        json_data = request.get_json(silent=True) or {}
        data_hex = json_data.get('data')

    if not data_hex:
        return {'error': 'Missing data parameter'}, 400

    try:
        data_bytes = bytes.fromhex(data_hex)
        result = marshal.loads(data_bytes)
        return {'result': result}
    except ValueError:
        return {'error': 'Invalid hex data'}, 400
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
