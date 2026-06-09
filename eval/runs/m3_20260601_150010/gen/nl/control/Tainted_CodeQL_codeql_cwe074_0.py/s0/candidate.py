from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)

# SSH connection configuration (can be modified as needed)
SSH_HOST = '127.0.0.1'
SSH_PORT = 22
SSH_USERNAME = 'user'
SSH_PASSWORD = 'password'

@app.route('/execute', methods=['POST'])
def execute_command():
    """Execute a command on remote SSH server and return standard output"""
    try:
        # Get command from request parameters (supports both JSON body and query string)
        if request.is_json:
            command = request.json.get('command')
        else:
            command = request.args.get('command')

        if not command:
            return jsonify({'error': 'No command parameter provided'}), 400

        # Create SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to remote SSH server
        ssh_client.connect(
            hostname=SSH_HOST,
            port=SSH_PORT,
            username=SSH_USERNAME,
            password=SSH_PASSWORD
        )

        # Execute the command on remote server
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # Read command output
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        # Close SSH connection
        ssh_client.close()

        # Return the command output
        return jsonify({
            'command': command,
            'stdout': output,
            'stderr': error,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'failed'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
