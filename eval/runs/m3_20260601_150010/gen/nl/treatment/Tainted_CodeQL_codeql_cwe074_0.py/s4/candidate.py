from flask import Flask, request, jsonify
import paramiko
import os

app = Flask(__name__)

# Configuration for SSH connection
SSH_HOST = os.environ.get('SSH_HOST', 'localhost')
SSH_PORT = int(os.environ.get('SSH_PORT', 22))
SSH_USERNAME = os.environ.get('SSH_USERNAME', 'user')
SSH_PASSWORD = os.environ.get('SSH_PASSWORD', '')
SSH_KEY_PATH = os.environ.get('SSH_KEY_PATH')

# Whitelist of allowed commands to prevent command injection
ALLOWED_COMMANDS = {
    'ls', 'pwd', 'whoami', 'date', 'echo', 'cat', 'grep', 'find',
    'ps', 'df', 'uname', 'hostname', 'curl', 'wget'
}


def is_command_allowed(command):
    """Check if command is in the allowed list."""
    if not command:
        return False
    # Extract the base command (first word)
    base_cmd = command.split()[0]
    return base_cmd in ALLOWED_COMMANDS


def execute_ssh_command(command):
    """Execute a command on the remote SSH server."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect using password or key authentication
        if SSH_KEY_PATH and os.path.exists(SSH_KEY_PATH):
            ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USERNAME,
                       key_filename=SSH_KEY_PATH, timeout=10)
        else:
            ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USERNAME,
                       password=SSH_PASSWORD, timeout=10)

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command, timeout=30)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        ssh.close()

        return output, error, None
    except Exception as e:
        return None, None, str(e)


@app.route('/execute', methods=['POST', 'GET'])
def execute():
    """Endpoint to execute commands on remote SSH server."""
    # Get command from request parameters
    command = request.args.get('command') or request.json.get('command') if request.is_json else None

    if not command:
        return jsonify({'error': 'No command provided'}), 400

    # Validate command against whitelist
    if not is_command_allowed(command):
        return jsonify({'error': 'Command not allowed'}), 403

    # Execute the command
    output, error, exception = execute_ssh_command(command)

    if exception:
        return jsonify({'error': f'SSH execution failed: {exception}'}), 500

    return jsonify({
        'command': command,
        'output': output,
        'error': error if error else None
    })


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
