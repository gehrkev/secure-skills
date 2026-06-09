from Crypto.Cipher import *
import hashlib

def generate_fingerprint(key, iv):
    '''
    Generate a fingerprint for the given key and iv.

    :param key: The key used for encryption.
    :param iv: The iv used for encryption.
    '''
    h = hashlib.sha256()
    h.update(key)
    h.update(iv)
    return h.hexdigest()
