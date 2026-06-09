from flask import Flask, request, jsonify
import paramiko
import os

app = Flask(__name__)

SSH_HOST = os.environ.get('SSH_HOST', 'localhost')
SSH_PORT = int(os.environ.get('SSH_PORT', 22))
SSH_USERNAME = os.environ.get('SSH_USERNAME', 'user')
SSH_PASSWORD = os.environ.get('SSH_PASSWORD', 'password')

ALLOWED_COMMANDS = {
    'date': '/bin/date',
    'whoami': '/usr/bin/whoami',
    'hostname': '/bin/hostname',
    'uptime': '/usr/bin/uptime',
    'pwd': '/bin/pwd',
}

def execute_remote_command(command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=SSH_HOST,
            port=SSH_PORT,
            username=SSH_USERNAME,
            password=SSH_PASSWORD,
            timeout=10
        )

        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        ssh.close()

        return output, error, None
    except Exception as e:
        return None, None, str(e)

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request body'}), 400

        command_name = data.get('command', '')

        if command_name not in ALLOWED_COMMANDS:
            return jsonify({'error': 'Command not allowed'}), 403

        command = ALLOWED_COMMANDS[command_name]
        output, error, exc = execute_remote_command(command)

        if exc:
            return jsonify({'error': exc}), 500

        return jsonify({
            'command': command_name,
            'output': output,
            'error': error
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)
