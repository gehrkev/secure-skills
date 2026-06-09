import os
import subprocess
import crypt

from flask import Flask, request

app = Flask(__name__)

@app.route('/change_password')
def change_password():
    '''
    Get the username and password from the request using 'username' and 'password'.
    Change the password of the user using usermod.
    :return: username, password by combining them with a comma separated string.
    '''
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return '', 400

    try:
        hashed_password = crypt.crypt(password)
        subprocess.run(['usermod', '-p', hashed_password, username], check=True, capture_output=True)
        return f"{username},{password}"
    except Exception:
        return '', 500
