import random
import string

# Generate 7 random letters
chars = random.choices(string.ascii_letters, k=7)
# Add 1 random digit to ensure numbers are included
chars.append(random.choice(string.digits))
# Shuffle the characters
random.shuffle(chars)
# Create and print the password
password = ''.join(chars)
print(password)
