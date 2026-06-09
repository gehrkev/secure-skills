from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    command = request.args.get('command') or request.form.get('command')

    if not command:
        return jsonify({'error': 'No command provided'}), 400

    try:
        args = command.split()
        result = subprocess.run(args, capture_output=True, text=True)
        return jsonify({
            'command': command,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
