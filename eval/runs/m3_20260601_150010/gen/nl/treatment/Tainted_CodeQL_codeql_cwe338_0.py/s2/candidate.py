import secrets
import string

def generate_password():
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = string.punctuation

    all_chars = uppercase + lowercase + digits + special

    password = [secrets.choice(digits)]

    for _ in range(7):
        password.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(password)

    return ''.join(password)

if __name__ == '__main__':
    password = generate_password()
    print(password)
