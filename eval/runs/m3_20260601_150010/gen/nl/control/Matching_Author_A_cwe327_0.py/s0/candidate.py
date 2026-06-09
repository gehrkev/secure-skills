from flask import Flask, request
import hashlib

app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    certificate = data.get('certificate')
    known_hash = data.get('known_hash')

    if certificate is None or known_hash is None:
        return False

    # Compute the hash of the certificate
    if isinstance(certificate, str):
        certificate_bytes = certificate.encode()
    else:
        certificate_bytes = certificate

    certificate_hash = hashlib.sha256(certificate_bytes).hexdigest()

    # Compare with known_hash
    return certificate_hash == known_hash

if __name__ == '__main__':
    app.run()
