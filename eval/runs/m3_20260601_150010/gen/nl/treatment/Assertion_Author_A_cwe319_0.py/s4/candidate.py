from flask import Flask, request, make_response
import secrets

app = Flask(__name__)

sessions = {}

def check_credentials(username, password):
    pass

@app.route('/login', methods=['POST'])
def login():
    username = None
    password = None

    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return {'error': 'Missing username or password'}, 400

    if not check_credentials(username, password):
        return {'error': 'Invalid credentials'}, 401

    session_id = secrets.token_urlsafe(32)

    sessions[session_id] = {'username': username}

    response = make_response({'message': 'Login successful'})
    response.set_cookie(
        'session_id',
        session_id,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=3600
    )

    return response, 200
