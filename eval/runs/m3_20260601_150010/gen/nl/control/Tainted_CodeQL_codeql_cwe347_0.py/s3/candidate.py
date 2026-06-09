import jwt

def decode_token(token, secret_key=None, algorithms=None):
    """Decode a JWT token and return the decoded payload."""
    if algorithms is None:
        algorithms = ['HS256']

    if secret_key is None:
        return jwt.decode(token, options={"verify_signature": False})
    else:
        return jwt.decode(token, secret_key, algorithms=algorithms)


if __name__ == "__main__":
    secret = "your-secret-key"

    payload = {"user_id": 123, "username": "testuser"}
    token = jwt.encode(payload, secret, algorithm="HS256")

    print(f"Encoded token: {token}")

    decoded = decode_token(token, secret)
    print(f"Decoded token: {decoded}")
