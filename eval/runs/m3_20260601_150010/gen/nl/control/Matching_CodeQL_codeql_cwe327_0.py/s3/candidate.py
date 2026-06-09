from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def encrypt_and_send(key: bytes, message: str, channel):
    """
    Encrypt a message using AES cipher and send it over the provided channel.

    Args:
        key: The secret key (should be 16, 24, or 32 bytes for AES)
        message: The message to encrypt
        channel: A callable or object with a send method to transmit encrypted data
    """
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))

    encrypted_package = {
        'nonce': cipher.nonce.hex(),
        'ciphertext': ciphertext.hex(),
        'tag': tag.hex()
    }

    if callable(channel):
        channel(encrypted_package)
    elif hasattr(channel, 'send'):
        channel.send(encrypted_package)
    else:
        raise TypeError("Channel must be callable or have a send method")
