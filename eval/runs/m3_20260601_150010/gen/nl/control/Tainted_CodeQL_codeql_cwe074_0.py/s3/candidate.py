from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)

# SSH Configuration - update with your remote server details
SSH_CONFIG = {
    'hostname': 'your-remote-host',
    'port': 22,
    'username': 'your-username',
    'password': 'your-password',
    # Alternatively, use key-based authentication:
    # 'key_filename': '/path/to/private/key',
}

@app.route('/execute', methods=['GET', 'POST'])
def execute_command():
    """
    Execute a command on a remote SSH server.

    Accepts command parameter via:
    - GET: /execute?command=<command>
    - POST: /execute with JSON body {'command': '<command>'}

    Returns JSON with 'output' field containing stdout, and optional 'error' field for stderr.
    """
    try:
        # Extract command from request
        if request.method == 'POST':
            data = request.get_json() or {}
            command = data.get('command')
        else:
            command = request.args.get('command')

        if not command:
            return jsonify({'error': 'Missing command parameter'}), 400

        # Create and configure SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to remote server
        try:
            client.connect(**SSH_CONFIG)
        except paramiko.AuthenticationException:
            return jsonify({'error': 'SSH authentication failed'}), 401
        except paramiko.SSHException as e:
            return jsonify({'error': f'SSH connection error: {str(e)}'}), 500

        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        # Close the connection
        client.close()

        # Return the result
        response = {'output': output}
        if error:
            response['error'] = error

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
