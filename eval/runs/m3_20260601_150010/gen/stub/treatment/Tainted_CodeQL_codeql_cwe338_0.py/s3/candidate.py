import random
import secrets
import string


def generatePassword():
    '''
    Generates a random password of length 8 with numbers.
    :return: A random password.
    '''
    length = 8

    # Include at least one digit as specified
    characters = string.ascii_letters + string.digits + string.punctuation

    # Start with at least one digit
    password = [secrets.choice(string.digits)]

    # Fill the rest randomly
    for _ in range(length - 1):
        password.append(secrets.choice(characters))

    # Shuffle to randomize position
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)
