import jwt


def decode_jwt(token, secret=None):
    if secret is None:
        return jwt.decode(token, options={"verify_signature": False})
    else:
        return jwt.decode(token, secret, algorithms=["HS256"])
