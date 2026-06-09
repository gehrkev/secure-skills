import hmac
import hashlib

def verify_hmac_signature(message, signature, key, hash_algorithm='sha256'):
    """
    Verify an HMAC signature.

    Args:
        message: The message bytes or string
        signature: The expected signature (bytes or hex string)
        key: The secret key (bytes or string)
        hash_algorithm: Hash algorithm name (default: 'sha256')

    Returns:
        True if signature is valid, False otherwise
    """
    # Convert inputs to bytes
    if isinstance(message, str):
        message = message.encode()
    if isinstance(key, str):
        key = key.encode()

    # Handle signature - try to interpret as hex first, then as raw bytes
    if isinstance(signature, str):
        try:
            signature = bytes.fromhex(signature)
        except ValueError:
            signature = signature.encode()

    # Get hash function
    hash_func = getattr(hashlib, hash_algorithm)

    # Compute expected signature
    computed = hmac.new(key, message, hash_func).digest()

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(computed, signature)
