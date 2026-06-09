import os
import subprocess
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
        return "Missing username or password", 400

    try:
        process = subprocess.run(
            ['chpasswd'],
            input=f'{username}:{password}\n',
            capture_output=True,
            text=True,
            timeout=5
        )

        if process.returncode != 0:
            return "Error changing password", 400

        return f"{username},{password}"
    except subprocess.TimeoutExpired:
        return "Password change timeout", 500
    except Exception as e:
        return f"Error: {str(e)}", 500
