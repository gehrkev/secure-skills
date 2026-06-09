from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def encrypt_and_send(secret_key, message, channel):
    """
    Encrypt a message using AES-256-GCM and send it over the provided channel.

    Args:
        secret_key: bytes, the secret key (32 bytes for AES-256)
        message: str or bytes, the message to encrypt
        channel: callable, a function that receives the encrypted data
    """
    # Convert message to bytes if needed
    if isinstance(message, str):
        message = message.encode('utf-8')

    # Validate key length
    if len(secret_key) != 32:
        raise ValueError("Secret key must be 32 bytes for AES-256")

    # Create AES-256-GCM cipher (provides both confidentiality and authenticity)
    cipher = AES.new(secret_key, AES.MODE_GCM)

    # Encrypt and generate authentication tag
    ciphertext, tag = cipher.encrypt_and_digest(message)

    # Prepare data to send: nonce + ciphertext + tag
    encrypted_data = cipher.nonce + ciphertext + tag

    # Send encrypted data through the channel
    channel(encrypted_data)


if __name__ == "__main__":
    # Generate a 256-bit key
    secret_key = get_random_bytes(32)

    # Define a simple channel (function that sends encrypted data)
    def simple_channel(data):
        print(f"Encrypted data sent ({len(data)} bytes): {data.hex()}")

    # Encrypt and send a message
    message = "Hello, World!"
    encrypt_and_send(secret_key, message, simple_channel)
