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
        return {'error': 'package parameter is required'}, 400

    if not all(c.isalnum() or c in '-_' for c in package):
        return {'error': 'Invalid package name'}, 400

    try:
        subprocess.run(['conda', 'install', '-y', package], check=True)
        return {'package': package}
    except subprocess.CalledProcessError as e:
        return {'error': f'Failed to install package: {str(e)}'}, 500
