from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def encrypt_aes_cbc(data: bytes) -> bytes:
    """
    Encrypt data using AES in CBC mode with a static IV and PKCS7 padding.

    Args:
        data: The plaintext bytes to encrypt

    Returns:
        The encrypted ciphertext bytes
    """
    # Static key (16 bytes for AES-128)
    key = b'0123456789abcdef'

    # Static initialization vector (16 bytes)
    iv = b'staticiv1234567!'

    # Pad the data to block size (128 bits = 16 bytes) using PKCS7
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Create cipher in CBC mode
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()

    # Encrypt the padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext


if __name__ == "__main__":
    plaintext = b"Hello, World!"
    encrypted = encrypt_aes_cbc(plaintext)
    print(f"Encrypted: {encrypted.hex()}")
