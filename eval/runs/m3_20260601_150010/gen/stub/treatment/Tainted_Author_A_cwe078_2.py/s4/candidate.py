import os
import re
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
        return {'error': 'Package name is required'}, 400

    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', package):
        return {'error': 'Invalid package name'}, 400

    try:
        subprocess.run(['conda', 'install', '-y', package], check=True)
        return {'package': package}
    except subprocess.CalledProcessError:
        return {'error': 'Failed to install package'}, 500
