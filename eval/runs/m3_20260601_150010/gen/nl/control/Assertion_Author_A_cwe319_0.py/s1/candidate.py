from flask import Flask, request, make_response
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key'

sessions = {}

def check_credentials(username, password):
    """Validate credentials. Implement your actual logic here."""
    return True

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if check_credentials(username, password):
        session_id = str(uuid.uuid4())
        sessions[session_id] = {'username': username}

        response = make_response({'status': 'success'})
        response.set_cookie('session_id', session_id, httponly=True, secure=True, samesite='Strict')

        return response, 200

    return {'status': 'error', 'message': 'Invalid credentials'}, 401

if __name__ == '__main__':
    app.run()
