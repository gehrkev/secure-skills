from flask import Flask, request, jsonify
import marshal

app = Flask(__name__)

@app.route('/unmarshal', methods=['GET', 'POST'])
def unmarshal_endpoint():
    hex_data = request.args.get('data') or request.form.get('data')

    if not hex_data:
        return jsonify({'error': 'Missing data parameter'}), 400

    try:
        byte_data = bytes.fromhex(hex_data)
        result = marshal.loads(byte_data)
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': f'Invalid hex: {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
