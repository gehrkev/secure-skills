from flask import Flask, request, jsonify
import subprocess
import shutil

app = Flask(__name__)

@app.route('/install', methods=['GET', 'POST'])
def install():
    # Get package name from request parameter
    package_name = request.args.get('package') or request.form.get('package')

    if not package_name:
        return jsonify({'error': 'package parameter is required'}), 400

    # Validate package name - reject if it contains shell metacharacters
    unsafe_chars = {' ', '\t', '\n', ';', '|', '&', '<', '>', '$', '`', '(', ')', '{', '}', '*', '?', '[', ']'}
    if any(c in package_name for c in unsafe_chars):
        return jsonify({'error': 'invalid package name'}), 400

    try:
        # Get fully-qualified path to conda for secure execution
        conda_path = shutil.which('conda')
        if not conda_path:
            return jsonify({'error': 'conda not found'}), 500

        # Use subprocess with list arguments to prevent command injection
        result = subprocess.run(
            [conda_path, 'install', '-y', package_name],
            capture_output=True,
            text=True,
            check=True
        )
        return jsonify({'package': package_name})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'failed to install package: {e.stderr}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
