import random
import secrets
import string


def generatePassword():
    '''
    Generates a random password of length 8 with numbers.
    :return: A random password.
    '''
    password = [secrets.choice(string.digits)]
    password.extend(secrets.choice(string.ascii_letters + string.digits) for _ in range(7))

    # Fisher-Yates shuffle using cryptographically secure random
    for i in range(len(password) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password[i], password[j] = password[j], password[i]

    return ''.join(password)
