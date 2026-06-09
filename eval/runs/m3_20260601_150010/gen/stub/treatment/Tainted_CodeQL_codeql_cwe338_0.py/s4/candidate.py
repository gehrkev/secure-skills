import random
import secrets
import string


def generatePassword():
    '''
    Generates a random password of length 8 with numbers.
    :return: A random password.
    '''
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(8))
    return password
