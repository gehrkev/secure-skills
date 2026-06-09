from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)

# SSH server configuration
SSH_HOST = "localhost"
SSH_PORT = 22
SSH_USERNAME = "user"
SSH_PASSWORD = "password"

# Whitelist of allowed commands to prevent command injection
ALLOWED_COMMANDS = [
    "ls",
    "pwd",
    "whoami",
    "uname -a",
    "df -h",
    "date",
]

def is_command_allowed(command):
    """Validate that the command is in the allowed whitelist"""
    return command.strip() in ALLOWED_COMMANDS

def execute_remote_command(command):
    """Execute command on remote SSH server and return output"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USERNAME, password=SSH_PASSWORD)
        stdin, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        return output, error, None
    except Exception as e:
        return None, None, str(e)
    finally:
        client.close()

@app.route('/execute', methods=['POST'])
def execute():
    """Endpoint that accepts a command parameter and executes it on remote SSH server"""
    try:
        data = request.get_json()
        command = data.get('command', '').strip()

        if not command:
            return jsonify({'error': 'Command parameter is required'}), 400

        if not is_command_allowed(command):
            return jsonify({'error': 'Command not allowed'}), 403

        output, error, exception = execute_remote_command(command)

        if exception:
            return jsonify({'error': exception}), 500

        return jsonify({'output': output, 'error': error}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1')
