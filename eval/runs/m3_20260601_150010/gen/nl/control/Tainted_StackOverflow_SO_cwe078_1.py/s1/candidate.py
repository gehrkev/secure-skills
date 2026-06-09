from flask import Flask, request
import subprocess
import sys

app = Flask(__name__)

@app.route('/install')
def install():
    package = request.args.get('package')
    if not package:
        return "Package name is required", 400

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return package
    except subprocess.CalledProcessError as e:
        return f"Failed to install {package}", 500

if __name__ == '__main__':
    app.run(debug=True)
