from flask import Flask, request
import hashlib

app = Flask(__name__)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    # Get certificate and known_hash from request
    if request.method == 'POST':
        data = request.get_json() or {}
        certificate = data.get('certificate')
        known_hash = data.get('known_hash')
    else:
        certificate = request.args.get('certificate')
        known_hash = request.args.get('known_hash')

    if certificate is None or known_hash is None:
        return False

    # Compute SHA256 hash of certificate
    if isinstance(certificate, str):
        cert_bytes = certificate.encode('utf-8')
    else:
        cert_bytes = certificate

    cert_hash = hashlib.sha256(cert_bytes).hexdigest()

    # Return True if hashes match, False otherwise
    return cert_hash == known_hash

if __name__ == '__main__':
    app.run()
