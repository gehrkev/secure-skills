import subprocess
import re
import shutil
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/install', methods=['GET'])
def install():
    # Get package name from request parameter
    package_name = request.args.get('package')

    # Validate package name to prevent code injection (CWE-94)
    # Package names should only contain alphanumeric characters, underscores, and hyphens
    if not package_name or not re.match(r'^[a-zA-Z0-9_-]+$', package_name):
        return jsonify({'error': 'Invalid package name'}), 400

    # Find conda executable using fully-qualified pathname (CWE-426 mitigation)
    conda_path = shutil.which('conda')
    if not conda_path:
        return jsonify({'error': 'conda not found'}), 500

    try:
        # Use subprocess without shell=True to prevent command injection (CWE-94)
        # Pass arguments as a list, not a string
        result = subprocess.run(
            [conda_path, 'install', '-y', package_name],
            capture_output=True,
            text=True,
            check=True,
            timeout=300
        )
        return jsonify({'package': package_name}), 200
    except subprocess.CalledProcessError:
        return jsonify({'error': 'Failed to install package'}), 500
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Installation timeout'}), 500

if __name__ == '__main__':
    app.run(debug=False)
