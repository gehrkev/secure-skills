from Crypto.Cipher import *
import hashlib

def generate_fingerprint(key, iv):
    '''
    Generate a fingerprint for the given key and iv.

    :param key: The key used for encryption.
    :param iv: The iv used for encryption.
    '''
    hasher = hashlib.sha256()
    hasher.update(key)
    hasher.update(iv)
    return hasher.digest()
