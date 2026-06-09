import subprocess
from flask import Flask, request
import shlex

app = Flask(__name__)

@app.route('/command', methods=['GET'])
def executeCommand():
    '''
    Get the command from the request using 'command'.
    Use subprocess.call to execute the command.
    Return the command.
    '''
    command = request.args.get('command', '')
    if command:
        subprocess.call(shlex.split(command))
    return command
