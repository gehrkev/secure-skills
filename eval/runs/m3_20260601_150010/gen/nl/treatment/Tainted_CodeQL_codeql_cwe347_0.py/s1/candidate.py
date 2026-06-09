import jwt
from typing import Dict, Any, Optional


def decode_jwt_token(token: str, secret: str, algorithms: list = None) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token and return the decoded payload.

    Args:
        token: The JWT token string to decode
        secret: The secret key used to verify the token
        algorithms: List of allowed algorithms (default: ['HS256'])

    Returns:
        The decoded token payload as a dictionary, or None if decoding fails
    """
    if algorithms is None:
        algorithms = ['HS256']

    try:
        decoded_token = jwt.decode(token, secret, algorithms=algorithms)
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Token is invalid: {e}")
        return None


def encode_jwt_token(payload: Dict[str, Any], secret: str) -> str:
    """
    Encode a payload into a JWT token.

    Args:
        payload: The data to encode in the JWT
        secret: The secret key to sign the token

    Returns:
        The encoded JWT token as a string
    """
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token


if __name__ == "__main__":
    secret_key = "your-secret-key"
    payload = {"user_id": 123, "username": "john_doe"}

    encoded_token = encode_jwt_token(payload, secret_key)
    print(f"Encoded token: {encoded_token}")

    decoded_token = decode_jwt_token(encoded_token, secret_key)
    print(f"Decoded token: {decoded_token}")
