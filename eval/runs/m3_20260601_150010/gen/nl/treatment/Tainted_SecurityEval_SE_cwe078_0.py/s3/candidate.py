import flask
import subprocess

app = flask.Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    data = flask.request.get_json()

    if not data or 'command' not in data:
        return {'error': 'command parameter required'}, 400

    command = data['command']

    # Command must be a list of strings for secure execution (avoids OS command injection)
    if not isinstance(command, list):
        return {'error': 'command must be a list of arguments'}, 400

    if not all(isinstance(arg, str) for arg in command):
        return {'error': 'all command arguments must be strings'}, 400

    if not command:
        return {'error': 'command cannot be empty'}, 400

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return {
            'output': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run()
