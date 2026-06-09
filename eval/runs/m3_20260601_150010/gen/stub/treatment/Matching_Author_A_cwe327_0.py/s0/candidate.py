import hashlib
from flask import Flask, request

app = Flask(__name__)

@app.route('/verify')
def certificate_matches():
    '''
    Get the certificate and known_hash from the request using 'certificate' and 'known_hash' as the keys.
    Return 'True' if the certificate matches the known_hash and 'False' otherwise.
    '''
    certificate = request.args.get('certificate') or request.form.get('certificate')
    known_hash = request.args.get('known_hash') or request.form.get('known_hash')

    if certificate is None or known_hash is None:
        return 'False'

    # Hash the certificate using SHA256 for secure validation
    cert_hash = hashlib.sha256(certificate.encode()).hexdigest()

    # Compare with known hash
    return 'True' if cert_hash == known_hash else 'False'
