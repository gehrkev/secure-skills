from Crypto.Cipher import AES
import base64


def encrypt_and_send(secret_key, message, channel):
    """
    Create a cipher from a secret key, encrypt a message,
    and send the encrypted result over the provided channel.

    Args:
        secret_key: Secret key as bytes or string
        message: Message to encrypt as bytes or string
        channel: Callable that receives the encrypted data package
    """
    # Convert to bytes if necessary
    if isinstance(secret_key, str):
        secret_key = secret_key.encode()
    if isinstance(message, str):
        message = message.encode()

    # Normalize key to 32 bytes for AES-256
    key = (secret_key * ((32 // len(secret_key)) + 1))[:32]

    # Create AES cipher in GCM mode
    cipher = AES.new(key, AES.MODE_GCM)

    # Encrypt message
    ciphertext = cipher.encrypt(message)
    tag = cipher.digest()
    nonce = cipher.nonce

    # Package encrypted data
    encrypted_data = {
        'nonce': base64.b64encode(nonce).decode(),
        'ciphertext': base64.b64encode(ciphertext).decode(),
        'tag': base64.b64encode(tag).decode()
    }

    # Send through channel
    channel(encrypted_data)


if __name__ == '__main__':
    def example_channel(data):
        print("Encrypted data sent through channel:")
        for key, value in data.items():
            print(f"  {key}: {value}")

    encrypt_and_send("secret_key", "Hello, World!", example_channel)
