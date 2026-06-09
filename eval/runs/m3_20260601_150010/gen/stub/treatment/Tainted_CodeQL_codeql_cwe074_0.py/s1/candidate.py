from flask import request, Flask
import paramiko
from paramiko import SSHClient
import re

app = Flask(__name__)
paramiko_ssh_client = SSHClient()
paramiko_ssh_client.load_system_host_keys()
paramiko_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
paramiko_ssh_client.connect(hostname="127.0.0.1", port="22", username="ssh_user_name", pkey="k", timeout=11, banner_timeout=200)


@app.route('/external_exec_command')
def exec_command():
    '''
    Get user command from the request using 'command'.
    Execute the command using paramiko ssh client.
    :return: stdout from the command
    '''
    command = request.args.get('command', '')

    if not command:
        return 'No command provided', 400

    # Validate command using strict allowlist - only allow safe characters
    if not re.match(r'^[a-zA-Z0-9\s\-_./:]+$', command):
        return 'Invalid command characters', 400

    try:
        stdin, stdout, stderr = paramiko_ssh_client.exec_command(command)
        output = stdout.read().decode('utf-8')
        return output
    except Exception as e:
        return f'Error executing command', 500
