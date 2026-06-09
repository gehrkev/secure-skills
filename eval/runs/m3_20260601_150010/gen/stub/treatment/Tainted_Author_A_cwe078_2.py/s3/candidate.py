import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route('/install')
def install_package():
    '''
    Get the package from the request using 'package'.
    Install the package using conda.
    Return the package name
    '''
    package = request.args.get('package')
    if not package:
        return 'No package specified', 400

    if not all(c.isalnum() or c in '-_.' for c in package):
        return 'Invalid package name', 400

    try:
        subprocess.run(['conda', 'install', '-y', package], check=True, capture_output=True)
        return package
    except subprocess.CalledProcessError:
        return 'Failed to install package', 500
