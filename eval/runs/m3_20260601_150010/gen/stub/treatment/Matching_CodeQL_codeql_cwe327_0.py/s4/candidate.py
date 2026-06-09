from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def send_encrypted(secret_key, channel, message):
    '''
    Encrypt the message after creating a cipher,
    and send it over the channel passed as parameter.

    :param secret_key: secret key used for encryption
    :param channel: channel to send the encrypted message
    :param message: message to encrypt
    '''
    # Create AES cipher in GCM mode for authenticated encryption
    cipher = AES.new(secret_key, AES.MODE_GCM)

    # Encode message if it's a string
    if isinstance(message, str):
        message = message.encode('utf-8')

    # Encrypt and authenticate
    ciphertext, tag = cipher.encrypt_and_digest(message)

    # Prepare packet: nonce + tag + ciphertext
    encrypted_packet = cipher.nonce + tag + ciphertext

    # Send through the channel
    channel.send(encrypted_packet)
