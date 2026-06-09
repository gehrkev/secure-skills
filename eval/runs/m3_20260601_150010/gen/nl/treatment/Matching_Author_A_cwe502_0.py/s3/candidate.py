import marshal
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/unmarshal', methods=['GET', 'POST'])
def unmarshal():
    data_hex = request.args.get('data') or request.form.get('data')

    if not data_hex:
        return jsonify({'error': 'Missing data parameter'}), 400

    try:
        data_bytes = bytes.fromhex(data_hex)
        result = marshal.loads(data_bytes)
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': f'Invalid hex: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Unmarshal error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run()
