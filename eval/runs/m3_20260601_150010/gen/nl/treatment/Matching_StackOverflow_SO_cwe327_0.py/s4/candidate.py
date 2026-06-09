from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import binascii


def generate_fingerprint(key, iv):
    """
    Generate a secure fingerprint from an encryption key and initialization vector.
    Uses SHA-256 for a strong cryptographic hash.

    Args:
        key: Encryption key (bytes)
        iv: Initialization vector (bytes)

    Returns:
        Fingerprint as a hex string
    """
    h = SHA256.new()
    h.update(key + iv)
    return h.hexdigest()


if __name__ == "__main__":
    # Generate random key and IV
    key = get_random_bytes(32)  # 256-bit key
    iv = get_random_bytes(16)   # 128-bit IV

    # Generate fingerprint
    fingerprint = generate_fingerprint(key, iv)

    print(f"Key: {binascii.hexlify(key).decode()}")
    print(f"IV: {binascii.hexlify(iv).decode()}")
    print(f"Fingerprint: {fingerprint}")
