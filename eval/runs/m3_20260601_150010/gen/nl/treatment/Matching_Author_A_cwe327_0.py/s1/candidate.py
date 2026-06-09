from flask import Flask, request, jsonify
import hashlib
from cryptography import x509
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()

    if not data or 'certificate' not in data or 'known_hash' not in data:
        return jsonify(False)

    try:
        certificate_pem = data['certificate']
        known_hash = data['known_hash']

        # Load and validate certificate
        cert_obj = x509.load_pem_x509_certificate(certificate_pem.encode())

        # Get DER encoding and hash
        cert_der = cert_obj.public_bytes(encoding=serialization.Encoding.DER)
        cert_hash = hashlib.sha256(cert_der).hexdigest()

        # Compare hashes
        match = cert_hash == known_hash

        return jsonify(match)

    except Exception:
        return jsonify(False)

if __name__ == '__main__':
    app.run()
