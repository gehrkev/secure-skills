import secrets
import string

def generate_password():
    characters = string.ascii_letters + string.digits
    digits = string.digits

    # Build password: 7 random chars + 1 digit
    password_list = [secrets.choice(characters) for _ in range(7)]
    password_list.append(secrets.choice(digits))

    # Shuffle using secrets for cryptographic randomness
    for i in range(len(password_list) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_list[i], password_list[j] = password_list[j], password_list[i]

    return ''.join(password_list)

if __name__ == '__main__':
    password = generate_password()
    print(password)
