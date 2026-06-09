import jwt


def decode_jwt_token(token, secret_key, algorithm='HS256'):
    """
    Decode and verify a JWT token.

    Args:
        token (str): The encoded JWT token string to decode
        secret_key (str): The secret key used to verify the token signature
        algorithm (str): The algorithm used for verification (default: HS256)

    Returns:
        dict: The decoded payload from the JWT token

    Raises:
        jwt.InvalidTokenError: If the token is invalid or signature verification fails
    """
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return decoded_payload
    except jwt.InvalidSignatureError as e:
        raise jwt.InvalidTokenError(f"Invalid token signature: {str(e)}")
    except jwt.DecodeError as e:
        raise jwt.InvalidTokenError(f"Failed to decode token: {str(e)}")
    except jwt.ExpiredSignatureError as e:
        raise jwt.InvalidTokenError(f"Token has expired: {str(e)}")
