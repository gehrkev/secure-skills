from flask import Flask, request, jsonify
import marshal
import hmac
import hashlib

app = Flask(__name__)

# Secret key for HMAC signature verification - should be loaded from environment in production
SECRET_KEY = b'your-secret-key'

@app.route('/unmarshal_config', methods=['GET', 'POST'])
def unmarshal_config():
    # Get config parameter from query string or JSON body
    config = request.args.get('config')
    if not config:
        data = request.get_json() or {}
        config = data.get('config')

    if not config:
        return jsonify({'error': 'Missing config parameter'}), 400

    # Get optional signature for verification (mitigation for CWE-502)
    signature = request.args.get('signature')
    if not signature:
        data = request.get_json() or {}
        signature = data.get('signature')

    try:
        # Verify HMAC signature if provided to ensure data integrity
        if signature:
            expected_sig = hmac.new(SECRET_KEY, config.encode(), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, expected_sig):
                return jsonify({'error': 'Invalid signature'}), 401

        # Decode from hex
        decoded_data = bytes.fromhex(config)

        # Unmarshal using marshal module
        result = marshal.loads(decoded_data)

        return jsonify({'result': result})

    except ValueError:
        return jsonify({'error': 'Invalid hex encoding'}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to unmarshal: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
