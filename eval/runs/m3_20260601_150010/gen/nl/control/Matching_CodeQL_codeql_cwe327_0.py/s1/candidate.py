from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad


def encrypt_message(key, message, channel):
    """
    Encrypt a message using AES cipher and send it through a channel.

    Args:
        key: Secret key (bytes, 16/24/32 bytes for AES-128/192/256)
        message: Message to encrypt (str or bytes)
        channel: Object with a send() method to transmit encrypted data
    """
    # Convert message to bytes if it's a string
    if isinstance(message, str):
        message = message.encode()

    # Create AES cipher in CBC mode with random IV
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    # Pad the message and encrypt
    padded_message = pad(message, AES.block_size)
    ciphertext = cipher.encrypt(padded_message)

    # Send IV and ciphertext through the channel
    channel.send(iv + ciphertext)
