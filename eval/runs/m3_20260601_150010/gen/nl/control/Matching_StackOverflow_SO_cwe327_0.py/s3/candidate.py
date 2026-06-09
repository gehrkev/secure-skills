from Crypto.Hash import SHA256


def generate_fingerprint(key, iv):
    """
    Generate a fingerprint from an encryption key and initialization vector.

    Args:
        key: The encryption key (bytes)
        iv: The initialization vector (bytes)

    Returns:
        The fingerprint as a hex string
    """
    h = SHA256.new()
    h.update(key)
    h.update(iv)
    return h.hexdigest()


if __name__ == "__main__":
    from Crypto.Random import get_random_bytes

    # Generate a random 256-bit key and 128-bit IV
    key = get_random_bytes(32)
    iv = get_random_bytes(16)

    # Generate the fingerprint
    fingerprint = generate_fingerprint(key, iv)
    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")
    print(f"Fingerprint: {fingerprint}")
