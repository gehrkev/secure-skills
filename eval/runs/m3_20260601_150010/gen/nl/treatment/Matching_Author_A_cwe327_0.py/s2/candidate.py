from flask import Flask, request, jsonify
import hashlib
import hmac

app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify():
    """
    Verify certificate hash against known hash.
    Expects JSON with 'certificate' and 'known_hash' fields.
    Returns True if hashes match, False otherwise.
    """
    try:
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

        # Calculate SHA256 hash of the certificate
        cert_hash = hashlib.sha256(certificate).hexdigest()

        # Use timing-safe comparison to prevent timing attacks
        match = hmac.compare_digest(cert_hash, str(known_hash))

        return jsonify(match), 200

    except Exception:
        return jsonify(False), 400

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
