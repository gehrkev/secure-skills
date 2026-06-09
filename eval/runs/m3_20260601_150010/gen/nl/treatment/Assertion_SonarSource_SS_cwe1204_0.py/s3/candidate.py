from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def encrypt_aes_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Encrypt data using AES in CBC mode with PKCS7 padding.

    Args:
        plaintext: The data to encrypt (bytes)
        key: The encryption key (16, 24, or 32 bytes for AES-128, AES-192, AES-256)
        iv: The static initialization vector (16 bytes for AES)

    Returns:
        The encrypted ciphertext (bytes)
    """
    # Validate key size
    if len(key) not in (16, 24, 32):
        raise ValueError("Key must be 16, 24, or 32 bytes for AES-128, AES-192, or AES-256")

    # Validate IV size
    if len(iv) != 16:
        raise ValueError("IV must be 16 bytes")

    # Apply PKCS7 padding
    block_size = 16
    padding_length = block_size - (len(plaintext) % block_size)
    padded_plaintext = plaintext + bytes([padding_length] * padding_length)

    # Create cipher and encryptor
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()

    # Encrypt the padded plaintext
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return ciphertext


if __name__ == "__main__":
    import os

    # Example: 256-bit key for AES-256
    key = os.urandom(32)

    # Static initialization vector (16 bytes)
    iv = b'\x00' * 16

    # Example plaintext
    plaintext = b"Hello, World!"

    # Encrypt
    ciphertext = encrypt_aes_cbc(plaintext, key, iv)
    print(f"Ciphertext: {ciphertext.hex()}")
