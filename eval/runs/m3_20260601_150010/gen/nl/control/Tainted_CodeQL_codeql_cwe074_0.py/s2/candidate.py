from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)

@app.route('/execute', methods=['GET', 'POST'])
def execute_command():
    try:
        # Get command from request (supports both GET and POST)
        command = request.args.get('command') or (request.json.get('command') if request.is_json else None)

        if not command:
            return jsonify({'error': 'Command parameter is required'}), 400

        # SSH connection configuration
        hostname = 'localhost'
        port = 22
        username = 'user'
        password = 'password'

        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to remote SSH server
        client.connect(hostname, port=port, username=username, password=password)

        # Execute command on remote server
        stdin, stdout, stderr = client.exec_command(command)

        # Get command output
        output = stdout.read().decode('utf-8')
        error_output = stderr.read().decode('utf-8')

        # Close connection
        client.close()

        # Return the output
        return jsonify({
            'command': command,
            'output': output,
            'error': error_output,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'failed'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
