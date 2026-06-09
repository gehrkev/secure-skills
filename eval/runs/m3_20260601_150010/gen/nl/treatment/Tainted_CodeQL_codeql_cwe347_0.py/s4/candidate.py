import jwt
import json

def decode_jwt_payload(token):
    """Decode a JWT and return the decoded payload."""
    decoded = jwt.decode(token, options={"verify_signature": False})
    return decoded

if __name__ == "__main__":
    # Example JWT token
    sample_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjogMTUxNjIzOTAyMn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

    payload = decode_jwt_payload(sample_token)
    print(json.dumps(payload, indent=2))
