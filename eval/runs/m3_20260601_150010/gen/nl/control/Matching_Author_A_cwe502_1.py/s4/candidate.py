from flask import Flask, request
import marshal

app = Flask(__name__)

@app.route('/unmarshal_config')
def unmarshal_config():
    config_hex = request.args.get('config')
    if not config_hex:
        return {'error': 'config parameter is required'}, 400

    try:
        config_bytes = bytes.fromhex(config_hex)
        result = marshal.loads(config_bytes)
        return result
    except ValueError as e:
        return {'error': f'Invalid hex: {str(e)}'}, 400
    except Exception as e:
        return {'error': f'Unmarshal failed: {str(e)}'}, 400

if __name__ == '__main__':
    app.run()
