import jwt


def encode_jwt(payload, secret_key='secret'):
    """
    Encodes a payload into a JWT token.

    Args:
        payload: Dictionary containing the data to encode
        secret_key: Secret key for signing the token

    Returns:
        JWT token as a string
    """
    return jwt.encode(payload, secret_key, algorithm='HS256')
