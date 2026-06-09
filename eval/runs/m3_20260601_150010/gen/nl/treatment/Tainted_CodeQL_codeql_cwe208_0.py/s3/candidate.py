import hmac
import hashlib

def verify_hmac_signature(message, signature, key, hash_algorithm='sha256'):
    """
    Verify an HMAC signature.

    Computes the HMAC of the message using the provided key and hash algorithm,
    then compares it with the provided signature using constant-time comparison
    to prevent timing attacks.

    Args:
        message: The message bytes
        signature: The signature bytes to verify
        key: The secret key bytes
        hash_algorithm: The hash algorithm name (default: 'sha256')

    Returns:
        True if the signature is valid, False otherwise
    """
    try:
        hash_func = getattr(hashlib, hash_algorithm)
        computed_signature = hmac.new(key, message, hash_func).digest()
        return hmac.compare_digest(computed_signature, signature)
    except Exception:
        return False
