from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/command', methods=['GET'])
def execute_command():
    command = request.args.get('command')
    if command:
        subprocess.call(command, shell=True)
    return command

if __name__ == '__main__':
    app.run()
