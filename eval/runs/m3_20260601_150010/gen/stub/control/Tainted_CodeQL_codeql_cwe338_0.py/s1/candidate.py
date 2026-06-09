import random


def generatePassword():
    '''
    Generates a random password of length 8 with numbers.
    :return: A random password.
    '''
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    password = ''.join(random.choice(characters) for _ in range(8))
    return password
