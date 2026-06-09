import secrets
import string

# Use cryptographically secure random generation
characters = string.ascii_letters + string.digits

# Generate 8 characters, ensuring at least one digit
while True:
    password = ''.join(secrets.choice(characters) for _ in range(8))
    if any(c.isdigit() for c in password):
        break

print(password)
