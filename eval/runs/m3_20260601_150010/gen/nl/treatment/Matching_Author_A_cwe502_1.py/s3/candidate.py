from flask import Flask, request, jsonify
import marshal

app = Flask(__name__)

@app.route('/unmarshal_config', methods=['GET', 'POST'])
def unmarshal_config():
    config = request.args.get('config') or request.form.get('config')

    if not config:
        return jsonify({'error': 'config parameter is required'}), 400

    try:
        config_bytes = bytes.fromhex(config)
        result = marshal.loads(config_bytes)
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': f'Invalid hex string: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Deserialization failed: {str(e)}'}), 400

if __name__ == '__main__':
    app.run()
