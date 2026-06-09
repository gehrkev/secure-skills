from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import os


def encrypt_and_send(secret_key, message, channel):
    """
    Create a cipher from a secret key, encrypt a message, and send over a channel.

    Uses AES-256-GCM for authenticated encryption, which provides both
    confidentiality and integrity protection.

    Args:
        secret_key: The secret key (bytes or str)
        message: The message to encrypt (bytes or str)
        channel: A callable or object with send() method to transmit encrypted data
    """
    if isinstance(message, str):
        message = message.encode('utf-8')

    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')

    if len(secret_key) < 32:
        secret_key = PBKDF2(secret_key, b'salt', dkLen=32, count=100000)
    else:
        secret_key = secret_key[:32]

    cipher = AES.new(secret_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message)

    encrypted_data = cipher.nonce + tag + ciphertext

    if callable(channel):
        channel(encrypted_data)
    elif hasattr(channel, 'send'):
        channel.send(encrypted_data)
    else:
        raise TypeError("channel must be callable or have a send() method")

    return encrypted_data


def decrypt_from_channel(secret_key, encrypted_data):
    """
    Decrypt data that was encrypted using encrypt_and_send.
    """
    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')

    if len(secret_key) < 32:
        secret_key = PBKDF2(secret_key, b'salt', dkLen=32, count=100000)
    else:
        secret_key = secret_key[:32]

    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    cipher = AES.new(secret_key, AES.MODE_GCM, nonce=nonce)
    message = cipher.decrypt_and_verify(ciphertext, tag)

    return message
