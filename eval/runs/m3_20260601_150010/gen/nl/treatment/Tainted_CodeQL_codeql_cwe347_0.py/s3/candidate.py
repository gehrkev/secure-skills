import jwt


def decode_jwt(token, secret=None, algorithms=None):
    """
    Decode a JWT token and return the decoded payload.

    Args:
        token: The JWT token string to decode
        secret: The secret key for verification (optional)
        algorithms: List of allowed algorithms (default: ["HS256"])

    Returns:
        The decoded JWT payload as a dictionary

    Raises:
        ValueError: If the token is invalid
    """
    try:
        if secret is None:
            decoded = jwt.decode(token, options={"verify_signature": False})
        else:
            if algorithms is None:
                algorithms = ["HS256"]
            decoded = jwt.decode(token, secret, algorithms=algorithms)
        return decoded
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid JWT token: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to decode JWT: {str(e)}")


if __name__ == "__main__":
    sample_token = jwt.encode({"user": "test", "id": 123}, "secret", algorithm="HS256")
    print(f"Encoded token: {sample_token}")

    decoded = decode_jwt(sample_token, "secret")
    print(f"Decoded payload: {decoded}")
