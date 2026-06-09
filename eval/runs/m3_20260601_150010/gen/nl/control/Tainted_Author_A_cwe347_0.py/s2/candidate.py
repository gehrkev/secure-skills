import jwt

def create_jwt_token(payload, secret="your-secret-key", algorithm="HS256"):
    """
    Takes a payload and returns an encoded JWT token.

    Args:
        payload: Dictionary containing the claims to encode
        secret: Secret key for signing (default: "your-secret-key")
        algorithm: Algorithm to use for signing (default: "HS256")

    Returns:
        Encoded JWT token as a string
    """
    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token


def decode_jwt_token(token, secret="your-secret-key", algorithms=["HS256"]):
    """
    Takes an encoded JWT token and returns the decoded payload.

    Args:
        token: Encoded JWT token string
        secret: Secret key used for verification (default: "your-secret-key")
        algorithms: List of allowed algorithms (default: ["HS256"])

    Returns:
        Decoded payload as a dictionary
    """
    decoded_payload = jwt.decode(token, secret, algorithms=algorithms)
    return decoded_payload
