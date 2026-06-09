import jwt
from typing import Dict, Any, Optional


def decode_jwt_payload(token: str, secret: Optional[str] = None, algorithms: Optional[list] = None) -> Dict[str, Any]:
    """
    Decode a JWT payload and return the decoded token.

    Args:
        token: The JWT token string to decode
        secret: Secret key for verifying the signature (optional)
        algorithms: List of allowed algorithms (default: ['HS256'])

    Returns:
        Dictionary containing the decoded payload
    """
    if algorithms is None:
        algorithms = ['HS256']

    if secret:
        decoded = jwt.decode(token, secret, algorithms=algorithms)
    else:
        decoded = jwt.decode(token, options={"verify_signature": False})

    return decoded
