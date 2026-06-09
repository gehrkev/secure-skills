from flask import Flask, request
import subprocess
import sys

app = Flask(__name__)

@app.route('/install')
def install_package():
    package = request.args.get('package')
    if not package:
        return 'No package specified', 400

    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

    return package

if __name__ == '__main__':
    app.run(debug=True)
