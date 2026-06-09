import random
import string

def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))

    if not any(c.isdigit() for c in password):
        password_list = list(password)
        password_list[0] = random.choice(string.digits)
        password = ''.join(password_list)

    return password

password = generate_password()
print(password)
