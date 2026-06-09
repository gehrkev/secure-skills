import hashlib


def check_certificate_hash(certificate, known_hash, algorithm='sha256'):
    """Check if a certificate matches a known hash.

    Args:
        certificate: The certificate as bytes or file path string
        known_hash: The known hash value to compare against
        algorithm: The hash algorithm to use (default: sha256)

    Returns:
        bool: True if computed hash matches known_hash, False otherwise
    """
    if isinstance(certificate, str):
        with open(certificate, 'rb') as f:
            certificate_data = f.read()
    else:
        certificate_data = certificate

    computed_hash = hashlib.new(algorithm, certificate_data).hexdigest()
    return computed_hash == known_hash
