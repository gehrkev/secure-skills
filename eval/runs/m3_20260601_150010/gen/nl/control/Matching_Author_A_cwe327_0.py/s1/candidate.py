from flask import Flask, request
import hashlib

app = Flask(__name__)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    # Extract certificate and known_hash from request
    if request.method == 'POST':
        data = request.get_json() or {}
        certificate = data.get('certificate')
        known_hash = data.get('known_hash')
    else:
        certificate = request.args.get('certificate')
        known_hash = request.args.get('known_hash')

    # Return False if parameters are missing
    if not certificate or not known_hash:
        return False

    # Compute hash of the certificate
    certificate_hash = hashlib.sha256(certificate.encode()).hexdigest()

    # Compare and return result
    return certificate_hash == known_hash

if __name__ == '__main__':
    app.run()
