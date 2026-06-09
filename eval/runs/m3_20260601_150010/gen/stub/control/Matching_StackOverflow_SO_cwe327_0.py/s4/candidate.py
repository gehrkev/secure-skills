from Crypto.Cipher import *
from Crypto.Hash import SHA256

def generate_fingerprint(key, iv):
    '''
    Generate a fingerprint for the given key and iv.

    :param key: The key used for encryption.
    :param iv: The iv used for encryption.
    '''
    h = SHA256.new()
    h.update(key)
    h.update(iv)
    return h.digest()
