from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/echo_name', methods=['GET', 'POST'])
def echo_name():
    name = request.args.get('name') or request.form.get('name')

    if not name:
        return jsonify({'error': 'Name parameter is required'}), 400

    # Validate name to prevent injection attacks
    if not isinstance(name, str) or len(name) > 100:
        return jsonify({'error': 'Invalid name parameter'}), 400

    # Only allow alphanumeric characters, spaces, hyphens, and apostrophes
    if not re.match(r'^[a-zA-Z0-9\s\-\']+$', name):
        return jsonify({'error': 'Invalid name format'}), 400

    greeting = f'Hello {name}!'
    return greeting

if __name__ == '__main__':
    app.run(debug=True)
