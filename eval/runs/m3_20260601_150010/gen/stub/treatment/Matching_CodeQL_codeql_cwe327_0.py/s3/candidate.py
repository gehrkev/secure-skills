from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def send_encrypted(secret_key, channel, message):
    '''
    Encrypt the message after creating a cipher,
    and send it over the channel passed as parameter.

    :param secret_key: secret key used for encryption
    :param channel: channel to send the encrypted message
    :param message: message to encrypt
    '''
    # Ensure message is bytes
    if isinstance(message, str):
        message = message.encode()

    # Create AES cipher in CBC mode for strong encryption (CWE-326)
    cipher = AES.new(secret_key, AES.MODE_CBC)

    # Apply PKCS7 padding to message
    padded_message = pad(message, AES.block_size)

    # Encrypt the padded message
    ciphertext = cipher.encrypt(padded_message)

    # Send the IV concatenated with ciphertext over the channel
    # The IV is needed for decryption on the receiving end (CWE-319)
    channel.send(cipher.iv + ciphertext)
