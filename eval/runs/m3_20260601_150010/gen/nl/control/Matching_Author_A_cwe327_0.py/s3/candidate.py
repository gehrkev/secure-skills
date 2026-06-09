from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()

    if not data or 'certificate' not in data or 'known_hash' not in data:
        return jsonify(False), 400

    certificate = data.get('certificate')
    known_hash = data.get('known_hash')

    # Compute the hash of the certificate
    cert_hash = hashlib.sha256(certificate.encode()).hexdigest()

    # Compare with known_hash
    return jsonify(cert_hash == known_hash)

if __name__ == '__main__':
    app.run(debug=True)
