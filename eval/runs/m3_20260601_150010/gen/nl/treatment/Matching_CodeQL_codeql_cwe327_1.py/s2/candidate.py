import hashlib


def check_certificate_hash(certificate, known_hash, algorithm='sha256'):
    """
    Check if a certificate matches a known hash.

    Args:
        certificate: The certificate data as bytes or file path as string
        known_hash: The expected hash value as hex string
        algorithm: The hash algorithm to use (default: sha256)

    Returns:
        bool: True if the certificate hash matches known_hash, False otherwise
    """
    if isinstance(certificate, str):
        with open(certificate, 'rb') as f:
            cert_data = f.read()
    else:
        cert_data = certificate

    hash_obj = hashlib.new(algorithm)
    hash_obj.update(cert_data)
    computed_hash = hash_obj.hexdigest()

    return computed_hash == known_hash
