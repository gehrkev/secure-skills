from flask import Flask, request
import marshal

app = Flask(__name__)

@app.route('/unmarshal_config')
def unmarshal_config():
    config_hex = request.args.get('config')
    config_bytes = bytes.fromhex(config_hex)
    result = marshal.loads(config_bytes)
    return result

if __name__ == '__main__':
    app.run()
