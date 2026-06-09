from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/execute_bash', methods=['GET', 'POST'])
def execute_bash():
    command = request.args.get('command') or request.form.get('command')

    if not command:
        return jsonify({'error': 'command parameter is required'}), 400

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
