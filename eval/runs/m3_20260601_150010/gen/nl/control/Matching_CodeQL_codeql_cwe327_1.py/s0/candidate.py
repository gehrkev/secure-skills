import hashlib


def check_certificate_hash(certificate_data, known_hash, algorithm='sha256'):
    """
    Check if a certificate matches a known hash.

    Args:
        certificate_data: The certificate data as bytes or file path string
        known_hash: The known hash value to compare against (hex string)
        algorithm: The hash algorithm to use (default: 'sha256')

    Returns:
        bool: True if the computed hash matches the known hash, False otherwise
    """
    # If certificate_data is a string, treat it as a file path and read it
    if isinstance(certificate_data, str):
        with open(certificate_data, 'rb') as f:
            certificate_data = f.read()

    # Compute the hash of the certificate
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(certificate_data)
    computed_hash = hash_obj.hexdigest()

    # Compare with the known hash
    return computed_hash.lower() == known_hash.lower()


if __name__ == '__main__':
    # Example usage
    certificate = b'example certificate data'

    # Compute hash for demonstration
    h = hashlib.sha256()
    h.update(certificate)
    known_hash = h.hexdigest()

    # Check if certificate matches the hash
    matches = check_certificate_hash(certificate, known_hash)
    print(f"Certificate matches hash: {matches}")
