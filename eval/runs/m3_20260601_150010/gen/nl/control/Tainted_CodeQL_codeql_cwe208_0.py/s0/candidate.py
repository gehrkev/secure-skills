import hmac
import hashlib


def verify_hmac_signature(message, signature, key, algorithm='sha256'):
    """
    Verify an HMAC signature by computing the HMAC of the message and comparing it
    with the provided signature.

    Args:
        message: The message as bytes or string
        signature: The signature to verify (hex string or bytes)
        key: The secret key (bytes or string)
        algorithm: Hash algorithm name (default: 'sha256')

    Returns:
        True if the computed signature matches the provided signature, False otherwise
    """
    # Convert inputs to bytes if needed
    if isinstance(message, str):
        message = message.encode()
    if isinstance(key, str):
        key = key.encode()

    # Compute the HMAC
    try:
        computed_signature = hmac.new(key, message, getattr(hashlib, algorithm)).digest()
    except AttributeError:
        return False

    # Convert signature to bytes if it's a hex string
    if isinstance(signature, str):
        try:
            signature = bytes.fromhex(signature)
        except ValueError:
            return False

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(computed_signature, signature)
