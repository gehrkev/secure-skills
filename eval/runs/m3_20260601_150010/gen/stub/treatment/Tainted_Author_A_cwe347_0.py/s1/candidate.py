import jwt


def jwt_decode(payload):
    '''
    Decode a payload into a JWT Token.
    :param payload: The payload to decode.
    :return: The decoded JWT Token.
    '''
    secret_key = 'your-secret-key'
    return jwt.encode(payload, secret_key, algorithm='HS256')
