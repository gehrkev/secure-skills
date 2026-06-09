import random
import string

characters = string.ascii_letters + string.digits
password_chars = [random.choice(string.digits)] + [random.choice(characters) for _ in range(7)]
random.shuffle(password_chars)
password = ''.join(password_chars)
print(password)
