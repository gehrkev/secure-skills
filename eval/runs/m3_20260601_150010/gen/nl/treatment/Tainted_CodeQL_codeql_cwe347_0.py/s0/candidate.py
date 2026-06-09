import jwt
import json
from typing import Dict, Any

def decode_jwt_token(token: str, secret: str = None, algorithms: list = None) -> Dict[str, Any]:
    """
    Decode a JWT token and return the decoded payload.

    Args:
        token: The JWT token string to decode
        secret: The secret key for verifying the token signature
        algorithms: List of allowed algorithms for decoding (defaults to ['HS256'])

    Returns:
        Dictionary containing the decoded payload

    Raises:
        jwt.InvalidTokenError: If the token is invalid or signature verification fails
    """
    if algorithms is None:
        algorithms = ['HS256']

    try:
        if secret:
            decoded_payload = jwt.decode(
                token,
                secret,
                algorithms=algorithms
            )
        else:
            decoded_payload = jwt.decode(
                token,
                options={"verify_signature": False}
            )

        return decoded_payload

    except jwt.InvalidTokenError as e:
        raise jwt.InvalidTokenError(f"Failed to decode token: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred while decoding the token: {str(e)}")


def main():
    sample_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    secret = "your-secret-key"

    try:
        decoded = decode_jwt_token(sample_token, secret)
        print("Decoded Token:")
        print(json.dumps(decoded, indent=2))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
