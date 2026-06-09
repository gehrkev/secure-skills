from flask import Flask, request, jsonify
import marshal

app = Flask(__name__)

@app.route('/unmarshal_config')
def unmarshal_config():
    config_hex = request.args.get('config')

    if not config_hex:
        return jsonify({'error': 'Missing config parameter'}), 400

    try:
        config_bytes = bytes.fromhex(config_hex)
        result = marshal.loads(config_bytes)
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': f'Invalid hex: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Unmarshal failed: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
