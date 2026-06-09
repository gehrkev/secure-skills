from flask import Flask, request, make_response
import secrets
from datetime import datetime

app = Flask(__name__)

def check_credentials(username, password):
    # Example implementation - in a real app, this would check a database
    # For now, we'll just accept any non-empty username/password
    return username and password

# Session storage (in production, use a database or session store like Redis)
sessions = {}

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Validate credentials using the existing check_credentials function
    if check_credentials(username, password):
        # Create a unique session ID
        session_id = secrets.token_hex(32)

        # Store the session
        sessions[session_id] = {
            'username': username,
            'created_at': datetime.now()
        }

        # Create the response
        response = make_response({'status': 'success', 'message': 'Login successful'})

        # Set the session ID in a cookie with secure flags
        response.set_cookie('session_id', session_id, httponly=True, secure=True, samesite='Lax')

        return response
    else:
        # Invalid credentials
        return {'status': 'error', 'message': 'Invalid credentials'}, 401

if __name__ == '__main__':
    app.run(debug=True)
