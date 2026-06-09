from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES


def generate_fingerprint(key, iv):
    """
    Generate a fingerprint from an encryption key and initialization vector.

    Args:
        key: The encryption key (bytes)
        iv: The initialization vector (bytes)

    Returns:
        A hexadecimal string representing the fingerprint
    """
    h = SHA256.new()
    h.update(key + iv)
    return h.hexdigest()


if __name__ == "__main__":
    # Generate a random AES-256 key and IV
    key = get_random_bytes(32)  # 256-bit key
    iv = get_random_bytes(16)   # 128-bit IV

    # Generate the fingerprint
    fingerprint = generate_fingerprint(key, iv)

    # Display results
    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")
    print(f"Fingerprint: {fingerprint}")
