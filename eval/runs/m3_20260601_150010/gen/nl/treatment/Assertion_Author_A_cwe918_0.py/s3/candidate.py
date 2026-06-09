import re
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_github_info', methods=['GET'])
def get_github_info():
    username = request.args.get('username', '').strip()

    if not username:
        return jsonify({'error': 'Username parameter is required'}), 400

    if not re.match(r'^[a-zA-Z0-9\-_]+$', username):
        return jsonify({'error': 'Invalid username format'}), 400

    if len(username) > 39:
        return jsonify({'error': 'Username too long'}), 400

    try:
        url = f'https://api.github.com/users/{username}'
        response = requests.get(url, timeout=5)

        if response.status_code == 404:
            return jsonify({'error': 'User not found'}), 404

        if response.status_code != 200:
            return jsonify({'error': 'GitHub API error'}), response.status_code

        return jsonify(response.json())

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Failed to fetch data'}), 500

if __name__ == '__main__':
    app.run(debug=False)
