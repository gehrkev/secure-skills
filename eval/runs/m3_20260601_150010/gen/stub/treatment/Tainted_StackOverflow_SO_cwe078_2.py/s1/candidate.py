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
    username = request.args.get('username') or request.form.get('username')
    password = request.args.get('password') or request.form.get('password')

    if not username or not password:
        return 'Missing credentials', 400

    try:
        hashed = crypt.crypt(password, crypt.METHOD_SHA512)
        subprocess.run(['usermod', '-p', hashed, username], check=True)
        return f"{username},{password}"
    except subprocess.CalledProcessError:
        return 'Failed to update password', 500
    except Exception as e:
        return f'Error: {str(e)}', 500
