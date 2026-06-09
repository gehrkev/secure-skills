from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

STATIC_IV = b'\x00' * 16
STATIC_KEY = b'\x00' * 32

def pad_data(data):
    block_size = 16
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def encrypt_aes_cbc(data, key=STATIC_KEY, iv=STATIC_IV):
    padded_data = pad_data(data)
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext

if __name__ == "__main__":
    plaintext = b"Hello, World!"
    encrypted = encrypt_aes_cbc(plaintext)
    print(f"Encrypted: {encrypted.hex()}")
