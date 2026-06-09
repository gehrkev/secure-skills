from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def is_valid_github_username(username):
    if not username or len(username) > 39:
        return False
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$'
    return re.match(pattern, username) is not None

@app.route('/get_github_info', methods=['GET'])
def get_github_info():
    username = request.args.get('username', '').strip()

    if not is_valid_github_username(username):
        return jsonify({'error': 'Invalid GitHub username'}), 400

    try:
        url = f'https://api.github.com/users/{username}'
        response = requests.get(url, timeout=5)

        if response.status_code == 404:
            return jsonify({'error': 'User not found'}), 404
        elif response.status_code != 200:
            return jsonify({'error': 'Failed to fetch user information'}), response.status_code

        return jsonify(response.json()), 200
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Failed to fetch user information'}), 500

if __name__ == '__main__':
    app.run(debug=False)
