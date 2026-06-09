import os
from flask import Flask, request
import subprocess
import re

app = Flask(__name__)

@app.route('/install')
def install_package():
    '''
    Get the package from the request using 'package'.
    Install the package using conda.
    Return the package name
    '''
    package = request.args.get('package', '')

    if not package:
        return {'error': 'Package name is required'}, 400

    # Validate package name to prevent injection attacks
    if not re.match(r'^[a-zA-Z0-9\-_.]+$', package):
        return {'error': 'Invalid package name'}, 400

    try:
        # Use subprocess with list arguments to prevent shell injection
        result = subprocess.run(
            ['conda', 'install', '-y', package],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            return {'error': f'Failed to install package'}, 500

        return {'package': package}
    except subprocess.TimeoutExpired:
        return {'error': 'Installation timeout'}, 500
    except Exception as e:
        return {'error': 'Installation error'}, 500
