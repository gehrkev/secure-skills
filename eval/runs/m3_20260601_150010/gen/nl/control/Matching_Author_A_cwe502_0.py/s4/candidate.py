from flask import Flask, request
import marshal

app = Flask(__name__)

@app.route('/unmarshal')
def unmarshal_endpoint():
    data = request.args.get('data')
    byte_data = bytes.fromhex(data)
    result = marshal.loads(byte_data)
    return result

if __name__ == '__main__':
    app.run()
