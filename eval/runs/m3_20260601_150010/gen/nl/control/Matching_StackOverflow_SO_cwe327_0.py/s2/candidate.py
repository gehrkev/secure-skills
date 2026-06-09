from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from binascii import hexlify


def generate_fingerprint(key, iv):
    """Generate a fingerprint from an encryption key and initialization vector."""
    combined = key + iv
    hash_obj = SHA256.new(combined)
    return hexlify(hash_obj.digest()).decode('utf-8')


if __name__ == "__main__":
    key = get_random_bytes(32)
    iv = get_random_bytes(16)

    fingerprint = generate_fingerprint(key, iv)

    print(f"Key: {hexlify(key).decode('utf-8')}")
    print(f"IV: {hexlify(iv).decode('utf-8')}")
    print(f"Fingerprint: {fingerprint}")
