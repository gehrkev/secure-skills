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
    cipher = AES.new(secret_key, AES.MODE_GCM)

    if isinstance(message, str):
        message = message.encode()

    ciphertext, tag = cipher.encrypt_and_digest(message)

    channel.send(cipher.nonce + tag + ciphertext)
