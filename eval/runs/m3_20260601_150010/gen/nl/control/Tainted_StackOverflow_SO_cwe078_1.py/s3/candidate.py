from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/install')
def install():
    package = request.args.get('package')
    if package:
        subprocess.run(['pip', 'install', package])
        return package
    return "No package specified"

if __name__ == '__main__':
    app.run()
