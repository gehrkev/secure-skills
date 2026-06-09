import jwt
from typing import Any, Dict

def decode_jwt_token(token: str, secret: str, algorithms: list = None) -> Dict[str, Any]:
    """
    Decode and verify a JWT token securely.

    Args:
        token: The JWT token string to decode
        secret: The secret key used to verify the signature
        algorithms: List of allowed algorithms (defaults to ["HS256"])

    Returns:
        The decoded payload as a dictionary

    Raises:
        jwt.InvalidTokenError: If the token is invalid or signature verification fails
        jwt.DecodeError: If the token cannot be decoded
        jwt.ExpiredSignatureError: If the token has expired
    """
    if algorithms is None:
        algorithms = ["HS256"]

    try:
        payload = jwt.decode(token, secret, algorithms=algorithms)
        return payload
    except (jwt.InvalidTokenError, jwt.DecodeError, jwt.ExpiredSignatureError) as e:
        raise jwt.InvalidTokenError(f"Failed to decode JWT token: {str(e)}")
