from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    certificate = data.get('certificate')
    known_hash = data.get('known_hash')

    if certificate is None or known_hash is None:
        return jsonify(False), 400

    if isinstance(certificate, str):
        cert_bytes = certificate.encode('utf-8')
    else:
        cert_bytes = certificate

    certificate_hash = hashlib.sha256(cert_bytes).hexdigest()

    result = certificate_hash == known_hash

    return jsonify(result)

if __name__ == '__main__':
    app.run()
