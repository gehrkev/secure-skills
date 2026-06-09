import jwt


def decode_token(token, secret=None):
    """
    Decode a JWT token and return the decoded payload.

    Args:
        token: The JWT token string to decode
        secret: Secret key for verification (optional). If None, decodes without verification.

    Returns:
        The decoded token payload as a dictionary
    """
    if secret:
        decoded = jwt.decode(token, secret, algorithms=['HS256'])
    else:
        decoded = jwt.decode(token, options={"verify_signature": False}, algorithms=['HS256'])

    return decoded


if __name__ == "__main__":
    # Example: Encode and decode a JWT token
    payload = {"user_id": 123, "username": "testuser", "email": "test@example.com"}
    secret = "secret_key_123"

    # Encode the token
    encoded_token = jwt.encode(payload, secret, algorithm="HS256")
    print(f"Encoded token: {encoded_token}")

    # Decode the token
    decoded_payload = decode_token(encoded_token, secret)
    print(f"Decoded payload: {decoded_payload}")
