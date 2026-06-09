import hashlib
import hmac


def verify_certificate_hash(certificate_data, known_hash, algorithm='sha256'):
    """
    Verify that a certificate matches a known hash value.

    Args:
        certificate_data: The certificate data as bytes
        known_hash: The expected hash value as a hex string
        algorithm: The hash algorithm to use (default: sha256)

    Returns:
        True if the certificate matches the known hash, False otherwise

    Raises:
        TypeError: If inputs are not of the correct type
        ValueError: If the hash algorithm is not supported
    """
    if not isinstance(certificate_data, bytes):
        raise TypeError("certificate_data must be bytes")
    if not isinstance(known_hash, str):
        raise TypeError("known_hash must be a string")

    try:
        hash_obj = hashlib.new(algorithm)
    except ValueError:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Compute the hash of the certificate
    hash_obj.update(certificate_data)
    computed_hash = hash_obj.hexdigest()

    # Normalize for comparison
    computed_hash_normalized = computed_hash.lower()
    known_hash_normalized = known_hash.lower()

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(computed_hash_normalized, known_hash_normalized)
