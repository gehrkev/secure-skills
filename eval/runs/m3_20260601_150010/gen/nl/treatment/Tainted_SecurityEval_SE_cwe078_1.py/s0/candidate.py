from flask import Flask, request, jsonify
import subprocess
import shlex

app = Flask(__name__)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    command = request.args.get('command') or request.form.get('command')

    if not command:
        return jsonify({'error': 'Command parameter is required'}), 400

    try:
        args = shlex.split(command)
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)

        return jsonify({
            'command': command,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command execution timed out'}), 504
    except FileNotFoundError:
        return jsonify({'error': 'Command not found'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
