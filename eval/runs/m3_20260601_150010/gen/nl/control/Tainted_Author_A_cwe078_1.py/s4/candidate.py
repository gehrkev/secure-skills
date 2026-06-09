from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/command', methods=['GET'])
def command():
    cmd = request.args.get('command')
    if cmd:
        subprocess.call(cmd, shell=True)
    return cmd

if __name__ == '__main__':
    app.run()
