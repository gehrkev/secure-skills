import jwt

def decode_jwt(token, secret='your-secret-key'):
    """
    Decodes a JWT token and returns the decoded payload.

    Args:
        token: The JWT token string to decode
        secret: The secret key used to verify the token (default: 'your-secret-key')

    Returns:
        The decoded payload as a dictionary
    """
    decoded = jwt.decode(token, secret, algorithms=['HS256'])
    return decoded
