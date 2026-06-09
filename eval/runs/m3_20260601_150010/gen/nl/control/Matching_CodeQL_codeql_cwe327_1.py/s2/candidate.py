import hashlib


def check_certificate_hash(certificate_data, known_hash):
    """
    Check if a certificate matches a known hash by computing the hash
    of the certificate using hashlib and comparing it to the known_hash value.

    Args:
        certificate_data: The certificate data as bytes
        known_hash: The known hash value as a string (hex format)

    Returns:
        bool: True if the computed hash matches the known_hash, False otherwise
    """
    computed_hash = hashlib.sha256(certificate_data).hexdigest()
    return computed_hash == known_hash
