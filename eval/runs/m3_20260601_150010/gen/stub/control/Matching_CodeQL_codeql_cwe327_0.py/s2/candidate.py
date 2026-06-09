from Crypto.Cipher import *
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad


def send_encrypted(secret_key, channel, message):
    '''
    Encrypt the message after creating a cipher,
    and send it over the channel passed as parameter.

    :param secret_key: secret key used for encryption
    :param channel: channel to send the encrypted message
    :param message: message to encrypt
    '''
    cipher = AES.new(secret_key, AES.MODE_CBC)

    if isinstance(message, str):
        message = message.encode()

    ciphertext = cipher.encrypt(pad(message, AES.block_size))

    channel.send(cipher.iv + ciphertext)
