import hmac
import hashlib

def verify_hmac(message, signature, key, hash_algorithm='sha256'):
    """
    Verify an HMAC signature by computing the HMAC of the message
    and comparing it with the provided signature.

    Args:
        message: The message (bytes)
        signature: The expected signature (bytes)
        key: The HMAC key (bytes)
        hash_algorithm: The hash algorithm to use (default: 'sha256')

    Returns:
        True if the signature is valid, False otherwise
    """
    computed_signature = hmac.new(key, message, getattr(hashlib, hash_algorithm)).digest()
    return hmac.compare_digest(computed_signature, signature)
