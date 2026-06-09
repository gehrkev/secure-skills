from flask import Flask, request, jsonify
import subprocess
import shlex

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.get_json()
        command = data.get('command')

        if not command:
            return jsonify({'error': 'No command provided'}), 400

        cmd_args = shlex.split(command) if isinstance(command, str) else command

        result = subprocess.run(cmd_args, capture_output=True, text=True, shell=False, timeout=30)

        return jsonify({
            'command': command,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command execution timeout'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
