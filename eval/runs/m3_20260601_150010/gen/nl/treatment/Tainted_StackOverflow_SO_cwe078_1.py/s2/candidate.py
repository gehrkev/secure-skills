from flask import Flask, request, jsonify
import subprocess
import sys
import re

app = Flask(__name__)

@app.route('/install', methods=['GET', 'POST'])
def install():
    package = request.args.get('package') or request.form.get('package')

    if not package:
        return jsonify({'error': 'package parameter is required'}), 400

    if not re.match(r'^[a-zA-Z0-9\-_.]+$', package):
        return jsonify({'error': 'invalid package name'}), 400

    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package],
            check=True,
            capture_output=True
        )
        return jsonify({'package': package})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'installation failed'}), 500

if __name__ == '__main__':
    app.run()
