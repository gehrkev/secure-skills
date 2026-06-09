from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes


def generate_fingerprint(key, iv):
    """
    Generate a fingerprint from an encryption key and initialization vector.

    Args:
        key: bytes - the encryption key
        iv: bytes - the initialization vector

    Returns:
        str - hexadecimal representation of the fingerprint
    """
    combined = key + iv
    h = SHA256.new(combined)
    return h.hexdigest()


if __name__ == "__main__":
    key = get_random_bytes(32)
    iv = get_random_bytes(16)

    fingerprint = generate_fingerprint(key, iv)

    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")
    print(f"Fingerprint: {fingerprint}")
