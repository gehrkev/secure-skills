from Crypto.Hash import SHA256

def generate_fingerprint(key, iv):
    """
    Generate a fingerprint from an encryption key and initialization vector.

    Args:
        key: The encryption key (bytes)
        iv: The initialization vector (bytes)

    Returns:
        The fingerprint as a hexadecimal string
    """
    h = SHA256.new()
    h.update(key)
    h.update(iv)
    return h.hexdigest()
