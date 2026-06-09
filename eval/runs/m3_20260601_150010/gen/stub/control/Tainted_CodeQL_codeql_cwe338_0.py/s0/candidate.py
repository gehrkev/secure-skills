import random


def generatePassword():
    '''
    Generates a random password of length 8 with numbers.
    :return: A random password.
    '''
    return ''.join(str(random.randint(0, 9)) for _ in range(8))
