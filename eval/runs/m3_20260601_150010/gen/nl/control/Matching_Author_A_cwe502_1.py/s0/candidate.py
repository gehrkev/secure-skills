from flask import Flask, request
import marshal

app = Flask(__name__)

@app.route('/unmarshal_config')
def unmarshal_config():
    config = request.args.get('config')
    if config is None:
        return {'error': 'config parameter is required'}, 400

    try:
        decoded = bytes.fromhex(config)
        result = marshal.loads(decoded)
        return result
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
