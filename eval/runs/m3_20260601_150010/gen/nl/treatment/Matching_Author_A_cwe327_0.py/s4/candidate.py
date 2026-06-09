from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    if not data:
        return jsonify(False), 400

    certificate = data.get('certificate')
    known_hash = data.get('known_hash')

    if not certificate or not known_hash:
        return jsonify(False), 400

    if isinstance(certificate, str):
        certificate_bytes = certificate.encode('utf-8')
    else:
        certificate_bytes = certificate

    cert_hash = hashlib.sha256(certificate_bytes).hexdigest()
    result = cert_hash == known_hash

    return jsonify(result)

if __name__ == '__main__':
    app.run()
