from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def encrypt_aes_cbc(data, key, iv):
    """
    Encrypt data using AES in CBC mode with PKCS7 padding.

    Args:
        data: bytes to encrypt
        key: encryption key (16, 24, or 32 bytes for AES-128/192/256)
        iv: initialization vector (16 bytes)

    Returns:
        encrypted ciphertext (bytes)
    """
    # PKCS7 padding
    block_size = 16
    padding_length = block_size - (len(data) % block_size)
    padded_data = data + bytes([padding_length]) * padding_length

    # Create AES cipher in CBC mode
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()

    # Encrypt padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext


if __name__ == "__main__":
    # Static key and IV
    key = b'\x00' * 16
    iv = b'\x00' * 16

    # Example plaintext
    plaintext = b"Hello, World!"

    # Encrypt
    ciphertext = encrypt_aes_cbc(plaintext, key, iv)
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext: {ciphertext.hex()}")
