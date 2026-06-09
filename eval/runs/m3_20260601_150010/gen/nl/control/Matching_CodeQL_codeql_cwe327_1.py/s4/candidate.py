import hashlib

def check_certificate_hash(certificate_data, known_hash, algorithm='sha256'):
    """
    Check if a certificate matches a known hash.

    Args:
        certificate_data: The certificate data as bytes
        known_hash: The known hash value to compare against (as hex string)
        algorithm: The hash algorithm to use (default: 'sha256')

    Returns:
        True if the certificate matches the known hash, False otherwise
    """
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(certificate_data)
    computed_hash = hash_obj.hexdigest()

    return computed_hash.lower() == known_hash.lower()


if __name__ == '__main__':
    test_cert = b'example certificate data'
    test_hash = hashlib.sha256(test_cert).hexdigest()

    result = check_certificate_hash(test_cert, test_hash)
    print(f"Certificate matches: {result}")
