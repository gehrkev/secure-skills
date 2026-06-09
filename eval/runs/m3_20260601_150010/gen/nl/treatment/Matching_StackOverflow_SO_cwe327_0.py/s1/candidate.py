from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes


def generate_fingerprint(key, iv):
    """
    Generate a fingerprint (hash) from an encryption key and initialization vector.

    Args:
        key: The encryption key (bytes)
        iv: The initialization vector (bytes)

    Returns:
        A hex-encoded fingerprint string
    """
    h = SHA256.new()
    h.update(key)
    h.update(iv)
    return h.hexdigest()


if __name__ == "__main__":
    key = get_random_bytes(32)
    iv = get_random_bytes(16)

    fingerprint = generate_fingerprint(key, iv)
    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")
    print(f"Fingerprint: {fingerprint}")
