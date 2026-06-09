from flask import Flask, request, jsonify
import subprocess
import shlex

app = Flask(__name__)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    # Get command from query parameters or JSON body
    if request.method == 'POST' and request.is_json:
        command = request.json.get('command')
    else:
        command = request.args.get('command')

    if not command:
        return jsonify({'error': 'No command parameter provided'}), 400

    try:
        # Use shlex.split to safely parse the command string into arguments
        # This prevents shell injection by avoiding shell=True
        args = shlex.split(command)
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)

        return jsonify({
            'command': command,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except FileNotFoundError:
        return jsonify({'error': 'Command not found'}), 404
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command execution timed out'}), 408
    except ValueError as e:
        return jsonify({'error': f'Invalid command syntax: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Command execution failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
