import jwt

def encode_jwt(payload, secret='your-secret-key', algorithm='HS256'):
    """
    Takes a payload and returns an encoded JWT token.

    Args:
        payload: Dictionary containing the claims to encode
        secret: Secret key for signing the token
        algorithm: Algorithm to use for encoding (default: HS256)

    Returns:
        A JWT token string
    """
    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token
