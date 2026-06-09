import jwt

def encode_jwt(payload, secret='your-secret-key', algorithm='HS256'):
    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token
