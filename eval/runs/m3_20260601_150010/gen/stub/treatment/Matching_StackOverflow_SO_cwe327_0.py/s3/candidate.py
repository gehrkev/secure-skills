from Crypto.Cipher import *
from Crypto.Hash import HMAC, SHA256

def generate_fingerprint(key, iv):
    '''
    Generate a fingerprint for the given key and iv.

    :param key: The key used for encryption.
    :param iv: The iv used for encryption.
    '''
    h = HMAC.new(key, digestmod=SHA256)
    h.update(iv)
    return h.hexdigest()
