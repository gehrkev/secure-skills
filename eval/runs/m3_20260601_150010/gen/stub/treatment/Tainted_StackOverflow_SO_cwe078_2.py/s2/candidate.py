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
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return "Error: missing username or password"

    try:
        subprocess.run(['usermod', '-p', password, username],
                      check=True,
                      capture_output=True)
        return f"{username},{password}"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.decode()}"
    except Exception as e:
        return f"Error: {str(e)}"
