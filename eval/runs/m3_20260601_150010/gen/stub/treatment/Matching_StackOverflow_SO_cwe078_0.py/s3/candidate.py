import subprocess
import os
import shlex

from flask import Flask, request

app = Flask(__name__)

@app.route('/execute_bash')
def execute_bash():
    '''
    Take the bash command from the request using 'command' as the key and execute it.
    Return the command.
    '''
    command = request.args.get('command') or request.form.get('command')

    if not command:
        return {'error': 'No command provided'}, 400

    try:
        args = shlex.split(command)
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)

        return {
            'command': command,
            'output': result.stdout,
            'error': result.stderr,
            'return_code': result.returncode
        }
    except Exception as e:
        return {'error': str(e), 'command': command}, 500
