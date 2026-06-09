from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes


def encrypt_and_send(secret_key, message, channel):
    """
    Encrypt a message using AES-256-GCM and send it over the provided channel.

    Args:
        secret_key: The secret key (bytes or str).
        message: The message to encrypt (bytes or str).
        channel: A callable that accepts the encrypted data (bytes).
    """
    if isinstance(message, str):
        message = message.encode('utf-8')

    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')

    salt = get_random_bytes(16)
    key = PBKDF2(secret_key, salt, dkLen=32, count=100000)

    cipher = AES.new(key, AES.MODE_GCM)

    ciphertext, tag = cipher.encrypt_and_digest(message)

    encrypted_data = salt + cipher.nonce + ciphertext + tag

    channel(encrypted_data)
