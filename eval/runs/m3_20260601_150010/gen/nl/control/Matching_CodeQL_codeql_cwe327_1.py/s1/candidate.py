import hashlib

def check_certificate_hash(certificate, known_hash, algorithm='sha256'):
    """
    Check if a certificate matches a known hash.

    Args:
        certificate: Certificate data as bytes or file path as string
        known_hash: Known hash value (hex string) to compare against
        algorithm: Hash algorithm to use (default: 'sha256')

    Returns:
        True if certificate hash matches known_hash, False otherwise
    """
    # Get certificate data
    if isinstance(certificate, str):
        with open(certificate, 'rb') as f:
            cert_data = f.read()
    else:
        cert_data = certificate

    # Compute hash using hashlib
    hasher = hashlib.new(algorithm)
    hasher.update(cert_data)
    computed_hash = hasher.hexdigest()

    # Compare with known hash
    return computed_hash == known_hash
