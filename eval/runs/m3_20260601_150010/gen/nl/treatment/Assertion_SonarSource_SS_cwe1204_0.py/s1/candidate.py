from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def encrypt_aes_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Encrypt data using AES in CBC mode with PKCS7 padding.

    Args:
        plaintext: The data to encrypt
        key: AES key (16, 24, or 32 bytes for AES-128/192/256)
        iv: Static initialization vector (16 bytes)

    Returns:
        Encrypted ciphertext with padding
    """
    block_size = 16

    padding_length = block_size - (len(plaintext) % block_size)
    padded_plaintext = plaintext + bytes([padding_length] * padding_length)

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return ciphertext


if __name__ == "__main__":
    key = b'0123456789abcdef'
    iv = b'fedcba9876543210'
    plaintext = b'Hello, World!'

    ciphertext = encrypt_aes_cbc(plaintext, key, iv)
    print(ciphertext.hex())
