from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    command = request.args.get('command') or request.form.get('command')

    if command is None:
        return jsonify({'error': 'No command provided'}), 400

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return jsonify({
            'command': command,
            'output': result.stdout,
            'error': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
