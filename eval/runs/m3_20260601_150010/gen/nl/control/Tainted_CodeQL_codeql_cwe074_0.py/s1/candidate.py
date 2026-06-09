from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)

# SSH configuration
SSH_HOST = 'localhost'
SSH_PORT = 22
SSH_USERNAME = 'user'
SSH_PASSWORD = 'password'


@app.route('/execute', methods=['GET', 'POST'])
def execute_command():
    """Execute a command on the remote SSH server and return output"""

    # Get command from request parameters
    if request.method == 'POST' and request.is_json:
        command = request.json.get('command')
    else:
        command = request.args.get('command')

    if not command:
        return jsonify({'error': 'No command provided'}), 400

    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to SSH server
        client.connect(
            hostname=SSH_HOST,
            port=SSH_PORT,
            username=SSH_USERNAME,
            password=SSH_PASSWORD,
            timeout=10
        )

        # Execute command
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8')

        # Close connection
        client.close()

        return jsonify({'output': output}), 200

    except paramiko.AuthenticationException:
        return jsonify({'error': 'Authentication failed'}), 401
    except paramiko.SSHException as e:
        return jsonify({'error': f'SSH error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
