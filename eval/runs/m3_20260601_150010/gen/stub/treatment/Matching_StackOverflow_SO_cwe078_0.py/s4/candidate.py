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
    command = request.args.get('command')
    if not command and request.is_json:
        command = request.json.get('command')

    if not command:
        return {'error': 'No command provided'}, 400

    try:
        args = shlex.split(command)
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)

        return {
            'command': command,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {'error': 'Command timed out'}, 500
    except Exception as e:
        return {'error': str(e)}, 500
