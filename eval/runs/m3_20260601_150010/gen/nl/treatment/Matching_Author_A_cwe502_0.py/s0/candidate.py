from flask import Flask, request, jsonify
import marshal

app = Flask(__name__)

@app.route('/unmarshal', methods=['GET', 'POST'])
def unmarshal_endpoint():
    data_hex = request.args.get('data')
    if not data_hex:
        return jsonify({'error': 'Missing data parameter'}), 400

    try:
        data_bytes = bytes.fromhex(data_hex)
        result = marshal.loads(data_bytes)
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': f'Invalid hex encoding: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Unmarshal failed: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
