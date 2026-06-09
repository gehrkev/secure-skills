from flask import Flask, request
import subprocess
import sys

app = Flask(__name__)

@app.route('/install')
def install():
    package = request.args.get('package')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    return package

if __name__ == '__main__':
    app.run()
