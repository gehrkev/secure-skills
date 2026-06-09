import hashlib
import hmac


def check_certificate_hash(certificate_data, known_hash, algorithm='sha256'):
    """
    Check if a certificate matches a known hash.

    Args:
        certificate_data: Certificate data as bytes or file path string
        known_hash: The expected hash value (hex string)
        algorithm: Hash algorithm to use (default: sha256)

    Returns:
        bool: True if certificate hash matches known_hash, False otherwise
    """
    # Handle file path input
    if isinstance(certificate_data, str):
        with open(certificate_data, 'rb') as f:
            certificate_data = f.read()

    # Validate certificate data is bytes
    if not isinstance(certificate_data, bytes):
        raise TypeError("certificate_data must be bytes or file path")

    # Compute the hash
    h = hashlib.new(algorithm)
    h.update(certificate_data)
    computed_hash = h.hexdigest()

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(computed_hash, known_hash.lower())
