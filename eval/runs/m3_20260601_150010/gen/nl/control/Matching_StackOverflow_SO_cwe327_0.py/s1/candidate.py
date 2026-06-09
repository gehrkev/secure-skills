from Crypto.Hash import SHA256
import os
import binascii

# Generate a random encryption key (256-bit)
key = os.urandom(32)

# Generate a random initialization vector (128-bit)
iv = os.urandom(16)

# Create a fingerprint from the key and IV by hashing them together
h = SHA256.new()
h.update(key + iv)
fingerprint = h.digest()

print(f"Key: {binascii.hexlify(key).decode()}")
print(f"IV: {binascii.hexlify(iv).decode()}")
print(f"Fingerprint: {binascii.hexlify(fingerprint).decode()}")
