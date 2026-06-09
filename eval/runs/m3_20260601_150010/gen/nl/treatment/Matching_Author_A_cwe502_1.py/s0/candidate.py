from flask import Flask, request, jsonify
import marshal
import binascii

app = Flask(__name__)

@app.route('/unmarshal_config', methods=['GET', 'POST'])
def unmarshal_config():
    try:
        # Get the 'config' parameter from the request
        config_hex = request.args.get('config') or request.form.get('config')

        if config_hex is None:
            return jsonify({'error': 'config parameter is required'}), 400

        # Decode from hex
        config_bytes = binascii.unhexlify(config_hex)

        # Unmarshal using the marshal module
        result = marshal.loads(config_bytes)

        return jsonify({'result': result})
    except binascii.Error:
        return jsonify({'error': 'Invalid hex format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
