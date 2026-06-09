from flask import Flask, request, jsonify
import subprocess
import shlex

app = Flask(__name__)

@app.route('/execute', methods=['POST', 'GET'])
def execute():
    # Get command from query parameters or POST JSON body
    command = request.args.get('command')

    if not command and request.is_json:
        command = request.get_json().get('command')

    if not command:
        return jsonify({'error': 'No command provided'}), 400

    try:
        # Parse command safely using shlex to handle quoting properly
        args = shlex.split(command)

        # Execute with shell=False (default) to prevent OS command injection
        result = subprocess.run(args, capture_output=True, text=True, timeout=10)

        return jsonify({
            'command': command,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command execution timed out'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to execute command: {str(e)}'}), 500

if __name__ == '__main__':
    app.run()
