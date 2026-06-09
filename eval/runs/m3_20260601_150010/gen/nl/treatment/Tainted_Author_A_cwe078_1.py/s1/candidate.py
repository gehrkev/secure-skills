from flask import Flask, request
import subprocess
import shlex

app = Flask(__name__)

@app.route('/command', methods=['GET'])
def execute_command():
    command = request.args.get('command', '')

    if not command:
        return {'error': 'command parameter is required'}, 400

    try:
        args = shlex.split(command)
        exit_code = subprocess.call(args)
        return {'command': command, 'exit_code': exit_code}
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run(debug=True)
