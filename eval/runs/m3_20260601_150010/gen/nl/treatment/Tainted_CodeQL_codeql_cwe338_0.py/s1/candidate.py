import secrets
import string

def generate_password():
    chars = [secrets.choice(string.ascii_letters) for _ in range(7)]
    chars.append(secrets.choice(string.digits))

    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]

    return ''.join(chars)

print(generate_password())
