import jwt


def jwt_decode(payload):
    '''
    Decode a payload into a JWT Token.
    :param payload: The payload to decode.
    :return: The decoded JWT Token.
    '''
    try:
        decoded = jwt.decode(payload, options={"verify_signature": False})
        return decoded
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {str(e)}")
