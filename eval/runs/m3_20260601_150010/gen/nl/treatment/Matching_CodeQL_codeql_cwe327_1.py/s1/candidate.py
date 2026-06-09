import hashlib


def check_certificate_hash(certificate_data, known_hash, algorithm='sha256'):
    """
    Check if a certificate matches a known hash by computing the hash of the
    certificate using hashlib and comparing it to the provided known_hash value.

    Args:
        certificate_data: The certificate data as bytes
        known_hash: The expected hash value as a hex string
        algorithm: The hash algorithm to use (default: sha256)

    Returns:
        True if the certificate hash matches the known hash, False otherwise
    """
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(certificate_data)
    computed_hash = hash_obj.hexdigest()

    return computed_hash.lower() == known_hash.lower()
