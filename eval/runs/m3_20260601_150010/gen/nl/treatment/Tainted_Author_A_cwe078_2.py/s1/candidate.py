from flask import Flask, request, jsonify
import subprocess
import re

app = Flask(__name__)

@app.route('/install', methods=['GET', 'POST'])
def install():
    package_name = request.args.get('package') or request.form.get('package')

    if not package_name:
        return jsonify({'error': 'package parameter is required'}), 400

    # Validate package name - only allow alphanumeric, dots, dashes, underscores
    if not re.match(r'^[a-zA-Z0-9._-]+$', package_name):
        return jsonify({'error': 'invalid package name'}), 400

    try:
        # Use subprocess with list argument to avoid shell injection
        result = subprocess.run(['conda', 'install', '-y', package_name],
                              capture_output=True, text=True, check=True)
        return jsonify({'package': package_name}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Failed to install package: {e.stderr}'}), 500

if __name__ == '__main__':
    app.run(debug=False)
