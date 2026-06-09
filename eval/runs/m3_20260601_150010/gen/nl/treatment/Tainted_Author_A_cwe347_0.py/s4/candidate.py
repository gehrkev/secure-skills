import jwt

def decode_jwt(token, secret, algorithm='HS256'):
    decoded_payload = jwt.decode(token, secret, algorithms=[algorithm])
    return decoded_payload
