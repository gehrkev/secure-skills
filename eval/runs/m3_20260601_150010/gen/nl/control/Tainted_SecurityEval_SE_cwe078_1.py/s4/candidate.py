from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    command = request.args.get('command')
    if not command and request.is_json:
        data = request.get_json()
        command = data.get('command') if data else None

    if not command:
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
