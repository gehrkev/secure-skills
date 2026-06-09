import hmac
import hashlib


def verify_hmac_signature(message, signature, key, algorithm='sha256'):
    """
    Verify an HMAC signature.

    Args:
        message: The message to verify (bytes or str)
        signature: The signature to verify against (bytes or hex string)
        key: The HMAC key (bytes or str)
        algorithm: The hash algorithm to use (default: 'sha256')

    Returns:
        True if the signature is valid, False otherwise
    """
    # Convert to bytes if needed
    if isinstance(message, str):
        message = message.encode()
    if isinstance(key, str):
        key = key.encode()
    if isinstance(signature, str):
        # Assume hex-encoded signature
        signature = bytes.fromhex(signature)

    # Compute HMAC with the specified algorithm
    hash_func = getattr(hashlib, algorithm)
    computed = hmac.new(key, message, hash_func).digest()

    # Compare using constant-time comparison to prevent timing attacks
    return hmac.compare_digest(computed, signature)
