from flask import Flask, request
import subprocess
import sys

app = Flask(__name__)

@app.route('/install')
def install():
    package = request.args.get('package')
    if not package:
        return 'package parameter is required', 400

    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', package],
        capture_output=True
    )

    if result.returncode != 0:
        return 'Failed to install package', 500

    return package

if __name__ == '__main__':
    app.run()
