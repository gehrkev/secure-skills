from flask import Flask, request, session, make_response
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

def check_credentials(username, password):
    return True

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password and check_credentials(username, password):
        session_id = secrets.token_urlsafe(32)
        session['user'] = username

        response = make_response({'status': 'success'})
        response.set_cookie(
            'session_id',
            session_id,
            httponly=True,
            secure=True,
            samesite='Strict'
        )

        return response, 200

    return {'status': 'failed'}, 401
