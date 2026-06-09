import hmac
import hashlib

def verify_hmac_signature(message, signature, key, hash_algorithm='sha256'):
    try:
        hash_func = getattr(hashlib, hash_algorithm)
        computed_signature = hmac.new(key, message, hash_func).digest()
        return hmac.compare_digest(computed_signature, signature)
    except (AttributeError, TypeError, ValueError):
        return False
