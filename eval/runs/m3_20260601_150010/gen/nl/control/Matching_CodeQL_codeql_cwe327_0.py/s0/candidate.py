from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import io


def encrypt_and_send(secret_key, message, channel):
    """
    Create a cipher from a secret key, encrypt a message, and send over channel.

    Args:
        secret_key: bytes object (16, 24, or 32 bytes for AES)
        message: str or bytes to encrypt
        channel: object with write() method
    """
    # Create cipher from secret key
    cipher = AES.new(secret_key, AES.MODE_EAX)

    # Convert message to bytes if needed
    if isinstance(message, str):
        message = message.encode()

    # Encrypt message
    ciphertext, tag = cipher.encrypt_and_digest(message)

    # Send encrypted result over channel
    channel.write(cipher.nonce)
    channel.write(tag)
    channel.write(ciphertext)


if __name__ == "__main__":
    # Example usage
    secret_key = get_random_bytes(32)  # 256-bit key
    message = "Hello, World!"

    # Use BytesIO as a channel
    channel = io.BytesIO()

    # Encrypt and send
    encrypt_and_send(secret_key, message, channel)

    # Retrieve encrypted data
    encrypted_data = channel.getvalue()
    print(f"Encrypted message sent over channel: {len(encrypted_data)} bytes")
