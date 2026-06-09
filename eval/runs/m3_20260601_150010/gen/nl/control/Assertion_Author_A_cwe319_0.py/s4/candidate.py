import uuid
from flask import Flask, request, make_response

app = Flask(__name__)

def check_credentials(username, password):
    """
    Validates username and password.
    Replace with actual credential validation logic.
    """
    valid_credentials = {
        'admin': 'password123',
        'user': 'user123'
    }
    return valid_credentials.get(username) == password

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if check_credentials(username, password):
        session_id = str(uuid.uuid4())
        response = make_response({'message': 'Login successful'})
        response.set_cookie('session_id', session_id)
        return response
    else:
        return {'message': 'Invalid credentials'}, 401

if __name__ == '__main__':
    app.run(debug=True)
