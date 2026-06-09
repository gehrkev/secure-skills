import random
import string

def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = [random.choice(string.digits)]
    password.extend(random.choice(characters) for _ in range(7))
    random.shuffle(password)
    return ''.join(password)

print(generate_password())
