import flask
import subprocess
import shlex

app = flask.Flask(__name__)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    command = flask.request.args.get('command') or (flask.request.json.get('command') if flask.request.json else None)

    if not command:
        return {'error': 'No command provided'}, 400

    try:
        args = shlex.split(command)
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)
        return {
            'output': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {'error': 'Command execution timed out'}, 500
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run()
