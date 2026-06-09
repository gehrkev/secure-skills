from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Static 256-bit key for AES-256
KEY = b'0123456789abcdef0123456789abcdef'

# Static 128-bit initialization vector
IV = b'0123456789abcdef'

def encrypt_data(plaintext):
    """
    Encrypt data using AES-256 in CBC mode with PKCS7 padding.

    Args:
        plaintext (bytes): The data to encrypt

    Returns:
        bytes: The encrypted ciphertext
    """
    # Apply PKCS7 padding to the plaintext
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Create AES cipher in CBC mode
    cipher = Cipher(
        algorithms.AES(KEY),
        modes.CBC(IV),
        backend=default_backend()
    )

    # Create encryptor and encrypt
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext


if __name__ == "__main__":
    # Example usage
    plaintext = b"Hello, World!"
    ciphertext = encrypt_data(plaintext)

    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext (hex): {ciphertext.hex()}")
