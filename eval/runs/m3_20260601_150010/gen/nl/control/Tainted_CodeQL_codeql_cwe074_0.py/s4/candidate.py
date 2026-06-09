from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)

@app.route('/execute', methods=['POST', 'GET'])
def execute_command():
    # Get command parameter from request
    if request.method == 'POST':
        command = request.json.get('command') if request.json else None
    else:
        command = request.args.get('command')

    if not command:
        return jsonify({'error': 'command parameter is required'}), 400

    # SSH connection details
    ssh_host = 'localhost'
    ssh_user = 'user'
    ssh_password = 'password'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to SSH server
        ssh.connect(ssh_host, username=ssh_user, password=ssh_password)

        # Execute command on remote server
        stdin, stdout, stderr = ssh.exec_command(command)

        # Get standard output
        output = stdout.read().decode('utf-8')

        return jsonify({'output': output})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        ssh.close()

if __name__ == '__main__':
    app.run(debug=True)
