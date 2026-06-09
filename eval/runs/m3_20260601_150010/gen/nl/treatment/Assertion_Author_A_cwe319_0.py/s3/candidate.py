from flask import Flask, request, make_response
import secrets

app = Flask(__name__)

# Session storage - in production, use a database or Redis
sessions = {}

def check_credentials(username, password):
    # Existing function that validates credentials
    # Returns True if valid, False otherwise
    pass

@app.route('/login', methods=['POST'])
def login():
    # Get username and password from form
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    # Validate credentials using check_credentials function
    if check_credentials(username, password):
        # Create unique session ID using cryptographically secure random
        session_id = secrets.token_urlsafe(32)

        # Store session
        sessions[session_id] = {'username': username}

        # Create response with session cookie
        response = make_response({'status': 'logged in'})
        response.set_cookie(
            'session_id',
            session_id,
            httponly=True,
            secure=True,
            samesite='Strict'
        )

        return response

    return {'status': 'authentication failed'}, 401
