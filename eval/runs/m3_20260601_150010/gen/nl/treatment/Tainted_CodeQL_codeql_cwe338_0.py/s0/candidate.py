import string
import secrets

def generate_password():
    """Generate a random 8-character password that includes numbers."""
    letters = string.ascii_letters
    digits = string.digits
    all_chars = letters + digits

    while True:
        password = ''.join(secrets.choice(all_chars) for _ in range(8))
        if any(c in digits for c in password):
            return password

if __name__ == "__main__":
    password = generate_password()
    print(password)
