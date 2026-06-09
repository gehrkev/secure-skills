import jwt

def decode_jwt_token(token, secret=None):
    """Decode a JWT token and return the decoded payload."""
    # If no secret provided, decode without signature verification
    options = {"verify_signature": False} if secret is None else {}

    decoded = jwt.decode(
        token,
        secret or "",
        algorithms=["HS256", "HS512", "RS256"],
        options=options
    )
    return decoded


if __name__ == "__main__":
    # Example: decode a JWT token
    sample_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

    result = decode_jwt_token(sample_token)
    print(result)
