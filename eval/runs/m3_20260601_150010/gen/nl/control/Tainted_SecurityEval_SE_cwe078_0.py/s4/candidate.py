from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    command = request.args.get('command') or request.form.get('command')

    if not command:
        return {'error': 'command parameter is required'}, 400

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {
            'output': result.stdout,
            'error': result.stderr,
            'returncode': result.returncode
        }
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run()
