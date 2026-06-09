from flask import Flask, request
import subprocess
import shlex

app = Flask(__name__)

@app.route('/command', methods=['GET'])
def execute_command():
    command = request.args.get('command', '')

    if not command:
        return {'error': 'No command provided'}, 400

    try:
        # Parse command string into arguments list for safer execution
        args = shlex.split(command)
        # Use subprocess.call without shell=True for safer execution (parameterization)
        return_code = subprocess.call(args)
        return {'command': command, 'return_code': return_code}
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
