from flask import Flask, request, make_response
import secrets

app = Flask(__name__)

sessions = {}

def check_credentials(username, password):
    pass

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    if check_credentials(username, password):
        session_id = secrets.token_urlsafe(32)
        sessions[session_id] = {'username': username}

        response = make_response({'status': 'success', 'message': 'Login successful'})
        response.set_cookie('session_id', session_id, httponly=True, secure=True, samesite='Strict')

        return response
    else:
        response = make_response({'status': 'error', 'message': 'Invalid credentials'}, 401)
        return response

if __name__ == '__main__':
    app.run()
