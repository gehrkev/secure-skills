from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def encrypt_aes_cbc(plaintext, key, iv):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext


if __name__ == "__main__":
    key = b'\x00' * 32
    iv = b'\x00' * 16
    plaintext = b"Hello, World!"

    ciphertext = encrypt_aes_cbc(plaintext, key, iv)
    print(f"Ciphertext: {ciphertext.hex()}")
