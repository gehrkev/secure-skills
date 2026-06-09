import hmac
import hashlib

def verify_hmac_signature(message, signature, key, hash_algorithm='sha256'):
    """
    Verify an HMAC signature.

    Args:
        message: The message to verify (bytes or str)
        signature: The signature to verify against (hex string or bytes)
        key: The secret key used to compute the signature (bytes or str)
        hash_algorithm: The hash algorithm used (default: 'sha256')

    Returns:
        True if the computed signature matches the provided signature, False otherwise
    """
    # Convert inputs to bytes if they are strings
    if isinstance(message, str):
        message = message.encode()
    if isinstance(key, str):
        key = key.encode()

    # Convert signature from hex if it's a string
    if isinstance(signature, str):
        try:
            signature = bytes.fromhex(signature)
        except ValueError:
            return False

    # Compute the expected HMAC
    hash_func = getattr(hashlib, hash_algorithm)
    computed_signature = hmac.new(key, message, hash_func).digest()

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(computed_signature, signature)
