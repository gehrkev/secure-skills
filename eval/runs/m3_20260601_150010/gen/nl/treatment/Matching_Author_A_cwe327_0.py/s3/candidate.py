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

    if certificate is None or known_hash is None:
        return jsonify(False), 400

    # Convert certificate to bytes if it's a string
    if isinstance(certificate, str):
        certificate = certificate.encode('utf-8')

    # Hash the certificate using SHA256
    cert_hash = hashlib.sha256(certificate).hexdigest()

    # Compare with known_hash
    return jsonify(cert_hash == known_hash)

if __name__ == '__main__':
    app.run()
