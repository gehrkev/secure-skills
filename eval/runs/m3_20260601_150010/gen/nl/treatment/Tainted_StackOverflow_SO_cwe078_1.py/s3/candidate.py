from flask import Flask, request
import subprocess
import sys

app = Flask(__name__)

@app.route('/install', methods=['GET', 'POST'])
def install():
    package = request.args.get('package')

    if not package:
        return {'error': 'package parameter is required'}, 400

    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
        return {'package': package}
    except subprocess.CalledProcessError:
        return {'error': 'Failed to install package'}, 500

if __name__ == '__main__':
    app.run()
