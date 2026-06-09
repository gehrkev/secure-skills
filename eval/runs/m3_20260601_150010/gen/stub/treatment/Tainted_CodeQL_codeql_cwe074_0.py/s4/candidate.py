from flask import request, Flask
import paramiko
from paramiko import SSHClient

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
        return {'error': 'Command parameter is required'}, 400

    # Whitelist of allowed commands to prevent command injection
    allowed_commands = ['ls', 'pwd', 'whoami', 'date', 'cat', 'grep', 'find', 'echo']
    command_base = command.split()[0] if command else ''

    if command_base not in allowed_commands:
        return {'error': 'Command not allowed'}, 403

    try:
        stdin, stdout, stderr = paramiko_ssh_client.exec_command(command)
        output = stdout.read().decode('utf-8')
        return {'output': output}
    except Exception as e:
        return {'error': str(e)}, 500
