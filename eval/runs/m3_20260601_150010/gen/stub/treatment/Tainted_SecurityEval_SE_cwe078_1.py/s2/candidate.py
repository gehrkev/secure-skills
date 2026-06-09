import os
import subprocess

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
        return {'error': 'Command is required'}, 400

    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            'command': command,
            'output': result.stdout,
            'returncode': result.returncode
        }
    except Exception as e:
        return {'error': str(e)}, 500
