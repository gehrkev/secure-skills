import subprocess
import shlex
from flask import Flask, request

app = Flask(__name__)

@app.route('/command', methods=['GET'])
def execute_command():
    command = request.args.get('command')
    if command:
        args = shlex.split(command)
        subprocess.call(args)
        return f"Command executed: {command}"
    return "No command provided"

if __name__ == '__main__':
    app.run()
