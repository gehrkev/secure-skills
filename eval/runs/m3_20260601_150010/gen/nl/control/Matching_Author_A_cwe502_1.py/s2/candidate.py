from flask import Flask, request
import marshal

app = Flask(__name__)

@app.route('/unmarshal_config')
def unmarshal_config():
    config = request.args.get('config')

    if not config:
        return {'error': 'config parameter required'}, 400

    try:
        decoded = bytes.fromhex(config)
        result = marshal.loads(decoded)
        return result
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
