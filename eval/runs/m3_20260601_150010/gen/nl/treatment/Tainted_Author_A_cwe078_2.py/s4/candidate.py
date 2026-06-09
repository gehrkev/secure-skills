from flask import Flask, request
import subprocess
import re
import shutil

app = Flask(__name__)

# Find conda path at startup
CONDA_PATH = shutil.which('conda')
if not CONDA_PATH:
    raise RuntimeError('conda not found in PATH')

@app.route('/install', methods=['GET', 'POST'])
def install_package():
    # Get package name from request
    package_name = request.args.get('package') or request.form.get('package')

    if not package_name:
        return 'Error: package parameter required', 400

    # Validate package name - only allow alphanumeric, dash, underscore, dot
    if not re.match(r'^[a-zA-Z0-9._-]+$', package_name):
        return 'Error: invalid package name', 400

    try:
        # Use fully qualified path for conda and subprocess list to prevent injection
        result = subprocess.run(
            [CONDA_PATH, 'install', '-y', package_name],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            return f'Error: installation failed\n{result.stderr}', 500

        return package_name, 200
    except Exception as e:
        return f'Error: installation error\n{str(e)}', 500

if __name__ == '__main__':
    app.run(debug=False)
