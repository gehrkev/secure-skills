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
        return 'No command specified', 400

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return 'Command timed out', 408
    except Exception as e:
        return f'Error: {str(e)}', 500
