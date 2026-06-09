import jwt


def decode_token(token, secret=None, algorithms=None):
    """Decode a JWT token and return the decoded payload."""
    if algorithms is None:
        algorithms = ['HS256']

    if secret is None:
        decoded = jwt.decode(token, options={"verify_signature": False})
    else:
        decoded = jwt.decode(token, secret, algorithms=algorithms)

    return decoded
