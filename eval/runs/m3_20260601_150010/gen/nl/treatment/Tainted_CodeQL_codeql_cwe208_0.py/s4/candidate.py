import hmac
import hashlib

def verify_hmac_signature(message, signature, key, algorithm='sha256'):
    """
    Verify an HMAC signature.

    Args:
        message: The message to verify (bytes or str)
        signature: The expected signature (hex string or bytes)
        key: The secret key used for HMAC (bytes or str)
        algorithm: The hash algorithm to use (default: 'sha256')

    Returns:
        True if the computed signature matches the provided signature, False otherwise
    """
    if isinstance(message, str):
        message = message.encode()
    if isinstance(key, str):
        key = key.encode()
    if isinstance(signature, str):
        try:
            signature = bytes.fromhex(signature)
        except ValueError:
            signature = signature.encode()

    computed = hmac.new(key, message, getattr(hashlib, algorithm)).digest()
    return hmac.compare_digest(computed, signature)
