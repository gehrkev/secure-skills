from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii

# Static initialization vector (16 bytes for AES)
STATIC_IV = b'\x00' * 16

# Static key (16 bytes for AES-128)
STATIC_KEY = b'0123456789abcdef'

def encrypt_aes_cbc(plaintext, key=STATIC_KEY, iv=STATIC_IV):
    """Encrypt data using AES in CBC mode with static IV and padding."""
    # Create cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the plaintext to block size (PKCS7)
    padded_plaintext = pad(plaintext, AES.block_size)

    # Encrypt
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext

if __name__ == "__main__":
    # Example usage
    plaintext = b"Hello, World!"
    ciphertext = encrypt_aes_cbc(plaintext)
    print(f"Encrypted: {binascii.hexlify(ciphertext).decode()}")
