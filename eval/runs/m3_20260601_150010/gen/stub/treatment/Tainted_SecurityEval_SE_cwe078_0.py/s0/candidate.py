import subprocess
import shlex
from flask import Flask, request

app = Flask(__name__)


@app.route('/execute')
def executeCommand():
    '''
    Get the command from the request using 'command'.
    Execute it and return the command.
    '''
    command = request.args.get('command')

    if not command:
        return {'error': 'No command provided'}, 400

    try:
        args = shlex.split(command)
        result = subprocess.run(args, capture_output=True, text=True)
        return {
            'command': command,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except Exception as e:
        return {'error': str(e)}, 500
