from flask import Flask, request, jsonify
import paramiko
import os

app = Flask(__name__)

# Whitelist of allowed commands to prevent command injection
ALLOWED_COMMANDS = {
    'whoami',
    'pwd',
    'ls',
    'date',
    'uname',
}

# SSH connection parameters (should be from environment variables in production)
SSH_HOST = os.getenv('SSH_HOST', 'localhost')
SSH_USER = os.getenv('SSH_USER', 'user')
SSH_PASSWORD = os.getenv('SSH_PASSWORD', 'password')
SSH_PORT = int(os.getenv('SSH_PORT', '22'))


@app.route('/execute', methods=['POST'])
def execute_command():
    """Execute a whitelisted command on the remote SSH server."""

    # Get command from request
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    command = data.get('command')
    if not command:
        return jsonify({'error': 'No command provided'}), 400

    # Validate command against whitelist to prevent command injection
    if command not in ALLOWED_COMMANDS:
        return jsonify({'error': 'Command not allowed'}), 403

    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to remote server
        ssh.connect(
            hostname=SSH_HOST,
            username=SSH_USER,
            password=SSH_PASSWORD,
            port=SSH_PORT,
            timeout=10
        )

        # Execute command
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        ssh.close()

        result = {'output': output}
        if error:
            result['error'] = error

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False)
