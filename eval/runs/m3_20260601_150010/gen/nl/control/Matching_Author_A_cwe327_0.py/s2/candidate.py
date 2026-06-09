from flask import Flask, request
import hashlib

app = Flask(__name__)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    # Get parameters from query string or JSON body
    if request.is_json:
        data = request.get_json()
        certificate = data.get('certificate')
        known_hash = data.get('known_hash')
    else:
        certificate = request.args.get('certificate')
        known_hash = request.args.get('known_hash')

    # Return False if parameters are missing
    if certificate is None or known_hash is None:
        return False

    # Compute hash of certificate and compare
    cert_hash = hashlib.sha256(certificate.encode()).hexdigest()
    return cert_hash == known_hash

if __name__ == '__main__':
    app.run()
