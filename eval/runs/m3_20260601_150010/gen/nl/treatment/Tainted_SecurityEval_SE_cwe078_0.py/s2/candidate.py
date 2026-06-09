from flask import Flask, request, jsonify
import subprocess
import shlex

app = Flask(__name__)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    command = request.args.get('command') or request.form.get('command')

    if not command:
        return jsonify({'error': 'command parameter is required'}), 400

    try:
        # Parse command string into argument list using shlex
        # Use subprocess.run with the argument list (no shell=True) to prevent command injection
        args = shlex.split(command)
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)

        return jsonify({
            'output': result.stdout,
            'error': result.stderr,
            'returncode': result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
