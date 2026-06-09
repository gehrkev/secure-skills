import secrets
import string


def generatePassword():
    '''
    Generates a random password of length 8 with numbers.
    :return: A random password.
    '''
    chars = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(chars) for _ in range(8))
    return password
