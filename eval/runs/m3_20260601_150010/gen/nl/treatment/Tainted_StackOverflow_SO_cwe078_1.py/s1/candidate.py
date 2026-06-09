import subprocess
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/install')
def install():
    package = request.args.get('package')

    if not package:
        return jsonify({'error': 'package parameter is required'}), 400

    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
        return jsonify({'package': package})
    except subprocess.CalledProcessError:
        return jsonify({'error': 'Failed to install package'}), 500

if __name__ == '__main__':
    app.run()
