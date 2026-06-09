import os
import sys
import subprocess

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
    if package:
        subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=False)
    return package
