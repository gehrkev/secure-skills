import random


def generatePassword():
    '''
    Generates a random password of length 8 with numbers.
    :return: A random password.
    '''
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    password = ''.join(random.choice(chars) for _ in range(8))
    return password
