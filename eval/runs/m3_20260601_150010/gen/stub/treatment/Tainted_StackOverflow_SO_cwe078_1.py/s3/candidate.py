import os
import subprocess
import sys
import re

from flask import Flask, request

app = Flask(__name__)


@app.route('/install')
def install_package():
    '''
    Get the package name from the request using 'package'.
    Install it using pip.
    Return the package name
    '''
    package = request.args.get('package')

    if not package:
        return 'Package name required', 400

    # Validate package name to prevent code injection (CWE-94)
    if not re.match(r'^[a-zA-Z0-9._-]+$', package):
        return 'Invalid package name', 400

    try:
        # Use explicit path with list args to avoid command injection (CWE-427)
        subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
    except subprocess.CalledProcessError:
        return 'Failed to install package', 500

    return package
