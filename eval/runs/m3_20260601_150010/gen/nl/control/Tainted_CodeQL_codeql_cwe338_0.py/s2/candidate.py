import random
import string

characters = string.ascii_letters + string.digits
password = [random.choice(string.digits)]
password += [random.choice(characters) for _ in range(7)]
random.shuffle(password)
print(''.join(password))
