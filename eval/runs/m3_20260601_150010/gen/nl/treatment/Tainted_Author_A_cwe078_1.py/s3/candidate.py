from flask import Flask, request
import subprocess
import shlex

app = Flask(__name__)

@app.route('/command', methods=['GET'])
def execute_command():
    command = request.args.get('command')
    if command:
        try:
            args = shlex.split(command)
            subprocess.call(args)
        except (ValueError, OSError):
            pass
    return command

if __name__ == '__main__':
    app.run()
