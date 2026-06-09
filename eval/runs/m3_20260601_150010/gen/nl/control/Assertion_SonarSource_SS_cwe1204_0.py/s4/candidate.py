from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Static key and initialization vector
KEY = b'0123456789ABCDEF'  # 16 bytes for AES-128
IV = b'ABCDEF0123456789'   # 16 bytes static IV

def pad_data(data: bytes, block_size: int = 16) -> bytes:
    """Pad data to block size using PKCS7 padding."""
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def encrypt_data(plaintext: bytes) -> bytes:
    """Encrypt data using AES in CBC mode with static IV."""
    padded_plaintext = pad_data(plaintext)

    cipher = Cipher(
        algorithms.AES(KEY),
        modes.CBC(IV),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return ciphertext

if __name__ == "__main__":
    plaintext = b"Hello, World!"
    ciphertext = encrypt_data(plaintext)
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext (hex): {ciphertext.hex()}")
