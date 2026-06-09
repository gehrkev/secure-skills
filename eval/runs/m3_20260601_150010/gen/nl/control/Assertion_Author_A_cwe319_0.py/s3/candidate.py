from flask import Flask, request, make_response
import secrets

app = Flask(__name__)

# Assumes check_credentials(username, password) is available
# Store sessions (use persistent storage in production)
sessions = {}


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if check_credentials(username, password):
        session_id = secrets.token_urlsafe(32)
        sessions[session_id] = username

        response = make_response({'status': 'success'})
        response.set_cookie('session_id', session_id)
        return response

    return {'error': 'Invalid credentials'}, 401


if __name__ == '__main__':
    app.run()
