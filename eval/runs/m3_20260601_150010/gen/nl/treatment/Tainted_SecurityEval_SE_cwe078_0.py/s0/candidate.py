from flask import Flask, request, jsonify
import subprocess
import shlex

app = Flask(__name__)

@app.route('/execute', methods=['POST', 'GET'])
def execute():
    command = request.args.get('command')

    if not command:
        return jsonify({'error': 'No command provided'}), 400

    try:
        args = shlex.split(command)
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except FileNotFoundError:
        return jsonify({'error': 'Command not found'}), 404
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
