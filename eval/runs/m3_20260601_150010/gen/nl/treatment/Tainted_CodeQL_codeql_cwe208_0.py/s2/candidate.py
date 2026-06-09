import hmac
import hashlib


def verify_hmac_signature(message, signature, key, hash_algorithm='sha256'):
    """
    Verify an HMAC signature by computing the HMAC of the message
    and comparing it with the provided signature.

    Args:
        message: The message to verify (bytes or str)
        signature: The expected signature (bytes or hex string)
        key: The secret key used for HMAC (bytes or str)
        hash_algorithm: The hash algorithm to use (default: 'sha256')

    Returns:
        True if the computed signature matches the provided signature, False otherwise
    """
    try:
        # Convert inputs to bytes if necessary
        if isinstance(message, str):
            message = message.encode()
        if isinstance(key, str):
            key = key.encode()

        # Handle signature as hex string or bytes
        if isinstance(signature, str):
            try:
                signature = bytes.fromhex(signature)
            except ValueError:
                signature = signature.encode()

        # Get the hash algorithm
        hash_func = getattr(hashlib, hash_algorithm)

        # Compute the HMAC of the message
        computed = hmac.new(key, message, hash_func)

        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(computed.digest(), signature)
    except (ValueError, AttributeError, TypeError):
        return False
