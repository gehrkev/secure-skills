from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import os


def encrypt_and_send(secret_key, message, channel):
    """
    Encrypts a message using AES-GCM with a secret key and sends it over a channel.

    Args:
        secret_key: The secret key (bytes or string)
        message: The message to encrypt (string or bytes)
        channel: A callable that accepts the encrypted data and sends it
    """
    # Convert inputs to bytes if needed
    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')
    if isinstance(message, str):
        message = message.encode('utf-8')

    # Derive a strong key from the secret using PBKDF2
    # Use a random salt and include it with the ciphertext
    salt = get_random_bytes(16)
    derived_key = PBKDF2(secret_key, salt, dkLen=32, count=100000)

    # Create AES-GCM cipher (authenticated encryption with strong confidentiality)
    cipher = AES.new(derived_key, AES.MODE_GCM)
    nonce = cipher.nonce  # 16 bytes for GCM

    # Encrypt the message
    ciphertext, tag = cipher.encrypt_and_digest(message)

    # Package: salt + nonce + tag + ciphertext
    encrypted_package = salt + nonce + tag + ciphertext

    # Send over the channel
    channel(encrypted_package)


def decrypt_from_channel(secret_key, encrypted_package):
    """
    Decrypts a message that was encrypted and packaged by encrypt_and_send.

    Args:
        secret_key: The secret key (bytes or string)
        encrypted_package: The encrypted package from the channel

    Returns:
        The decrypted message as bytes
    """
    # Convert secret_key to bytes if needed
    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')

    # Extract components
    salt = encrypted_package[:16]
    nonce = encrypted_package[16:32]
    tag = encrypted_package[32:48]
    ciphertext = encrypted_package[48:]

    # Derive the same key using the salt
    derived_key = PBKDF2(secret_key, salt, dkLen=32, count=100000)

    # Decrypt using AES-GCM
    cipher = AES.new(derived_key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    return plaintext
