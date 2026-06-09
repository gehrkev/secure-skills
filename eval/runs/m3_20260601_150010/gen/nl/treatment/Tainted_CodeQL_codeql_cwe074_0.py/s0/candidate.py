from flask import Flask, request, jsonify
import paramiko
import os

app = Flask(__name__)

ALLOWED_COMMANDS = [
    'ls',
    'pwd',
    'whoami',
    'date',
    'uname -a',
    'df -h',
    'ps aux',
]

SSH_HOST = os.getenv('SSH_HOST', 'localhost')
SSH_PORT = int(os.getenv('SSH_PORT', '22'))
SSH_USER = os.getenv('SSH_USER', 'user')
SSH_KEY_PATH = os.getenv('SSH_KEY_PATH', '/home/user/.ssh/id_rsa')


def validate_command(command):
    """Validate command against whitelist to prevent command injection."""
    for allowed in ALLOWED_COMMANDS:
        if command.strip() == allowed or command.strip().startswith(allowed + ' '):
            return True
    return False


def execute_ssh_command(command):
    """Execute command on remote SSH server and return output."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(
            hostname=SSH_HOST,
            port=SSH_PORT,
            username=SSH_USER,
            key_filename=SSH_KEY_PATH,
            timeout=10
        )

        stdin, stdout, stderr = client.exec_command(command, timeout=30)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        client.close()

        return {
            'success': True,
            'output': output,
            'error': error if error else None
        }
    except Exception as e:
        return {
            'success': False,
            'output': None,
            'error': str(e)
        }


@app.route('/execute', methods=['POST'])
def execute_command():
    """Endpoint to execute command on remote SSH server."""
    command = request.args.get('command', '').strip()

    if not command:
        return jsonify({
            'success': False,
            'error': 'Command parameter is required'
        }), 400

    if not validate_command(command):
        return jsonify({
            'success': False,
            'error': 'Command not in allowed commands list'
        }), 403

    result = execute_ssh_command(command)

    if result['success']:
        return jsonify({
            'success': True,
            'output': result['output'],
            'error': result['error']
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
