from Crypto.Cipher import *
from Crypto.Hash import SHA256
import hmac

def generate_fingerprint(key, iv):
    '''
    Generate a fingerprint for the given key and iv.

    :param key: The key used for encryption.
    :param iv: The iv used for encryption.
    '''
    return hmac.new(key, msg=iv, digestmod=SHA256).digest()
