from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/get_github_info', methods=['GET', 'POST'])
def get_github_info():
    # Get username from request
    username = request.args.get('username') or request.form.get('username')

    # Validate username - GitHub usernames can only contain alphanumeric characters and hyphens
    if not username or not re.match(r'^[a-zA-Z0-9\-]+$', username):
        return jsonify({'error': 'Invalid username format'}), 400

    # Query GitHub API with the validated username
    try:
        response = requests.get(f'https://api.github.com/users/{username}', timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'User not found'}), response.status_code
    except requests.RequestException:
        return jsonify({'error': 'Failed to fetch data from GitHub API'}), 500

if __name__ == '__main__':
    app.run(debug=True)
