import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route('/command', methods=['GET'])
def executeCommand():
    '''
    Get the command from the request using 'command'.
    Use subprocess.call to execute the command.
    Return the command.
    '''
    command = request.args.get('command')
    if not command:
        return 'No command provided', 400

    args = command.split()

    try:
        result = subprocess.call(args)
        return f'Command executed with return code: {result}'
    except Exception as e:
        return f'Error executing command: {str(e)}', 500
