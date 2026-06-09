from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


def encrypt_and_send(secret_key, message, channel):
    """
    Create a cipher from a secret key, encrypt a message, and send it over a channel.

    Args:
        secret_key: The secret key (bytes or str)
        message: The message to encrypt (bytes or str)
        channel: A file-like object with write() method or a callable
    """
    # Convert message to bytes if needed
    if isinstance(message, str):
        message = message.encode()

    # Convert key to bytes if needed
    if isinstance(secret_key, str):
        secret_key = secret_key.encode()

    # Ensure key is the proper length for AES (16, 24, or 32 bytes)
    if len(secret_key) not in [16, 24, 32]:
        secret_key = PBKDF2(secret_key, b'', dkLen=32)

    # Create cipher using AES in EAX mode (authenticated encryption)
    cipher = AES.new(secret_key, AES.MODE_EAX)

    # Encrypt the message and generate authentication tag
    ciphertext, tag = cipher.encrypt_and_digest(message)

    # Prepare encrypted data: nonce + tag + ciphertext
    encrypted_data = cipher.nonce + tag + ciphertext

    # Send through the channel
    if hasattr(channel, 'write'):
        channel.write(encrypted_data)
    elif callable(channel):
        channel(encrypted_data)
    else:
        raise ValueError("Channel must have a write() method or be callable")
