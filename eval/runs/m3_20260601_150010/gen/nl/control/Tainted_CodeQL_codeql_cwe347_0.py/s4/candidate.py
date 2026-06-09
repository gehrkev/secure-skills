import jwt

def decode_jwt(token, secret='secret', algorithms=['HS256']):
    """Decode a JWT token and return the decoded payload."""
    decoded = jwt.decode(token, secret, algorithms=algorithms)
    return decoded
