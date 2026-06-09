import jwt

def encode_payload_to_jwt(payload, secret='your-secret-key', algorithm='HS256'):
    """
    Encodes a payload into a JWT token.

    Args:
        payload: Dictionary containing the payload to encode
        secret: Secret key for signing the token
        algorithm: Algorithm for signing (default: HS256)

    Returns:
        JWT token as a string
    """
    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token


def decode_jwt_token(token, secret='your-secret-key', algorithm='HS256'):
    """
    Decodes a JWT token and returns the payload.

    Args:
        token: JWT token string to decode
        secret: Secret key for verification
        algorithm: Algorithm used for signing (default: HS256)

    Returns:
        Decoded payload as a dictionary
    """
    decoded_payload = jwt.decode(token, secret, algorithms=[algorithm])
    return decoded_payload
