import hashlib

def check_certificate_hash(certificate_data, known_hash, algorithm='sha256'):
    """
    Check if a certificate matches a known hash.

    Args:
        certificate_data: The certificate as bytes
        known_hash: The known hash value as a hex string
        algorithm: The hash algorithm to use (default: 'sha256')

    Returns:
        bool: True if the certificate matches the known hash, False otherwise
    """
    computed_hash = hashlib.new(algorithm, certificate_data).hexdigest()
    return computed_hash == known_hash.lower()
