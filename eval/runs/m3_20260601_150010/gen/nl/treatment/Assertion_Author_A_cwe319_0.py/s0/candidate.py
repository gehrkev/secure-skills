from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

# Session storage (in production, use a persistent database)
sessions = {}


@app.route('/login', methods=['POST'])
def login():
    # Initialize variables securely - avoid implicit defaults
    username = None
    password = None
    is_valid = False

    # Extract credentials from request form
    if 'username' in request.form:
        username = request.form.get('username')
    if 'password' in request.form:
        password = request.form.get('password')

    # Validate credentials using existing check_credentials function
    if username and password:
        is_valid = check_credentials(username, password)

    # If credentials are valid, create a session
    if is_valid:
        # Generate a cryptographically unique session ID
        session_id = secrets.token_urlsafe(32)

        # Store session in session store
        sessions[session_id] = {'username': username}

        # Create response and set session cookie
        response = jsonify({'status': 'success'})
        response.set_cookie(
            'session_id',
            session_id,
            secure=True,
            httponly=True,
            samesite='Lax'
        )
        return response

    # Invalid credentials
    return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401


if __name__ == '__main__':
    app.run()
