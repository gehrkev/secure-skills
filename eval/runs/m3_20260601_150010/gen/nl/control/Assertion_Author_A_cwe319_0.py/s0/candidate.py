from flask import Flask, request, jsonify, make_response
import uuid

app = Flask(__name__)

sessions = {}

def check_credentials(username, password):
    """Validate user credentials."""
    return True

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    if check_credentials(username, password):
        session_id = str(uuid.uuid4())
        sessions[session_id] = {'username': username}

        response = make_response(jsonify({'success': True}))
        response.set_cookie('session_id', session_id, httponly=True)
        return response

    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run()
