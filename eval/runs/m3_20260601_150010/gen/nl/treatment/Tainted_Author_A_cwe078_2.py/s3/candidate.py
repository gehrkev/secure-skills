from flask import Flask, request, jsonify
import subprocess
import re
import os

app = Flask(__name__)

@app.route('/install', methods=['GET', 'POST'])
def install():
    package_name = request.args.get('package') or request.form.get('package')

    if not package_name:
        return jsonify({'error': 'package parameter is required'}), 400

    # Validate package name to prevent injection attacks
    if not re.match(r'^[a-zA-Z0-9_.-]+$', package_name):
        return jsonify({'error': 'invalid package name'}), 400

    # Use fully-qualified path to conda executable
    conda_path = None
    for path in ['/opt/conda/bin/conda', '/usr/local/bin/conda', '/usr/bin/conda']:
        if os.path.exists(path):
            conda_path = path
            break

    if not conda_path:
        return jsonify({'error': 'conda not found'}), 500

    try:
        result = subprocess.run(
            [conda_path, 'install', '-y', package_name],
            capture_output=True,
            timeout=300
        )

        if result.returncode != 0:
            return jsonify({'error': 'installation failed'}), 500

        return jsonify({'package': package_name}), 200
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'installation timeout'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
