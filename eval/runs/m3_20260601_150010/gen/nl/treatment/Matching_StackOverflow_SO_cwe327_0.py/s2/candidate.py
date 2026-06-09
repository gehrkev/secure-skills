from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes


def generate_fingerprint(key, iv):
    """
    Generate a fingerprint from an encryption key and initialization vector.

    Args:
        key: Encryption key (bytes)
        iv: Initialization vector (bytes)

    Returns:
        str: Hexadecimal fingerprint
    """
    h = SHA256.new()
    h.update(key)
    h.update(iv)
    return h.hexdigest()


def main():
    key = get_random_bytes(32)
    iv = get_random_bytes(16)

    fingerprint = generate_fingerprint(key, iv)

    print(f"Key (hex): {key.hex()}")
    print(f"IV (hex): {iv.hex()}")
    print(f"Fingerprint: {fingerprint}")


if __name__ == "__main__":
    main()
