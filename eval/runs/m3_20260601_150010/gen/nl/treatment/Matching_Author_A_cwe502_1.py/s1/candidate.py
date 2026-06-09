import flask
import marshal

app = flask.Flask(__name__)

@app.route('/unmarshal_config')
def unmarshal_config():
    config = flask.request.args.get('config')
    if config is None:
        return {'error': 'config parameter required'}, 400

    try:
        data = bytes.fromhex(config)
        result = marshal.loads(data)
        return result
    except Exception:
        return {'error': 'Failed to process config'}, 400

if __name__ == '__main__':
    app.run()
