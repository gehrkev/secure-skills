from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def encrypt_and_send(secret_key, message, channel):
    """
    Create a cipher from a secret key, encrypt a message, and send it over a channel.

    Args:
        secret_key: Secret key for AES encryption (16, 24, or 32 bytes)
        message: Message to encrypt (str or bytes)
        channel: Channel object with a send(data) method
    """
    # Convert message to bytes if needed
    if isinstance(message, str):
        message = message.encode('utf-8')

    # Generate random IV for CBC mode
    iv = get_random_bytes(16)

    # Create AES cipher from secret key
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)

    # Pad and encrypt the message
    padded_message = pad(message, AES.block_size)
    ciphertext = cipher.encrypt(padded_message)

    # Send IV + ciphertext over channel
    # (IV must be transmitted so recipient can decrypt)
    encrypted_data = iv + ciphertext
    channel.send(encrypted_data)
