import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

GITHUB_API_BASE = "https://api.github.com"

@app.route('/get_github_info', methods=['GET'])
def get_github_info():
    username = request.args.get('username')

    if not username:
        return jsonify({'error': 'Username parameter is required'}), 400

    if not all(c.isalnum() or c in '-_' for c in username):
        return jsonify({'error': 'Invalid username format'}), 400

    url = f"{GITHUB_API_BASE}/users/{username}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'error': 'Failed to fetch user information'}), 500
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Failed to fetch user information'}), 500

if __name__ == '__main__':
    app.run(debug=True)
