import hmac
import hashlib

def verify_hmac_signature(message, signature, key, hash_algorithm='sha256'):
    """Verify an HMAC signature.

    Args:
        message: The message to verify (bytes or str)
        signature: The signature to verify against (bytes or hex str)
        key: The secret key used for HMAC (bytes or str)
        hash_algorithm: The hash algorithm to use (default: 'sha256')

    Returns:
        True if the signature is valid, False otherwise
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

    computed = hmac.new(key, message, getattr(hashlib, hash_algorithm)).digest()
    return hmac.compare_digest(computed, signature)
