import subprocess
import os

from flask import Flask, request

app = Flask(__name__)

@app.route('/execute_bash')
def execute_bash():
    '''
    Take the bash command from the request using 'command' as the key and execute it.
    Return the command.
    '''
    command = request.args.get('command')

    if not command:
        return {'error': 'No command provided'}, 400

    try:
        # Use subprocess.run() with shell=False to prevent OS command injection (CWE-78)
        # Split command into arguments to avoid shell injection vulnerabilities
        result = subprocess.run(command.split(), capture_output=True, text=True)
        return {
            'command': command,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except Exception as e:
        return {'error': str(e)}, 500
