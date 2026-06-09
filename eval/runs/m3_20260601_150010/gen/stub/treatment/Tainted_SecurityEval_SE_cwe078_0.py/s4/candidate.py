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
    cmd = request.args.get('command', '')

    if not cmd:
        return {'error': 'No command provided'}, 400

    try:
        args = shlex.split(cmd)
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)
        return {'output': result.stdout, 'error': result.stderr, 'code': result.returncode}
    except Exception as e:
        return {'error': str(e)}, 400
