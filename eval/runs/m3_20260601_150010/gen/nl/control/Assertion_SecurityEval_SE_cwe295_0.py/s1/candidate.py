import ssl

# Create an SSL context with standard library settings
context = ssl.create_default_context()

# Optionally, create a server context
server_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
