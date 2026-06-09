from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


def encrypt_aes_cbc(plaintext, key, iv):
    """
    Encrypt data using AES in CBC mode with PKCS7 padding.

    Args:
        plaintext: bytes to encrypt
        key: encryption key (16, 24, or 32 bytes for AES-128, AES-192, AES-256)
        iv: static initialization vector (16 bytes for AES)

    Returns:
        ciphertext (bytes)
    """
    if not isinstance(plaintext, bytes):
        plaintext = plaintext.encode()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext


def decrypt_aes_cbc(ciphertext, key, iv):
    """
    Decrypt data using AES in CBC mode.

    Args:
        ciphertext: encrypted data (bytes)
        key: encryption key (16, 24, or 32 bytes for AES-128, AES-192, AES-256)
        iv: static initialization vector (16 bytes for AES)

    Returns:
        plaintext (bytes)
    """
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext


if __name__ == "__main__":
    key = b'0123456789abcdef'
    iv = b'0123456789abcdef'
    plaintext = b'Hello, World!!!'

    encrypted = encrypt_aes_cbc(plaintext, key, iv)
    print(f"Encrypted: {encrypted.hex()}")

    decrypted = decrypt_aes_cbc(encrypted, key, iv)
    print(f"Decrypted: {decrypted}")
