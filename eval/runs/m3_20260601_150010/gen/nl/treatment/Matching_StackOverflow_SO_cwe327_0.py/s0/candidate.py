from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes


def generate_fingerprint(key, iv):
    """
    Generate a fingerprint from an encryption key and initialization vector.

    Args:
        key: The encryption key (bytes)
        iv: The initialization vector (bytes)

    Returns:
        A hexadecimal fingerprint string
    """
    hash_obj = SHA256.new()
    hash_obj.update(key)
    hash_obj.update(iv)
    return hash_obj.hexdigest()


if __name__ == "__main__":
    key = get_random_bytes(32)
    iv = get_random_bytes(16)

    fingerprint = generate_fingerprint(key, iv)
    print(f"Key fingerprint: {fingerprint}")
