import jwt

def jwt_decode(payload):
    '''
    Decode a payload into a JSON Web Token.
    :param payload: The payload to decode.
    :return: The decoded JSON Web Token.
    '''
    try:
        decoded = jwt.decode(payload, options={"verify_signature": False})
        return decoded
    except (jwt.InvalidTokenError, TypeError, ValueError) as e:
        raise ValueError("Invalid JWT token") from e
